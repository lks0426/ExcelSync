# ExcelSync AWS ECS 部署指南

## 🎯 概述

本指南将帮助你将ExcelSync应用部署到AWS ECS（Elastic Container Service），实现自动化CI/CD流程。

## 🏗️ 架构设计

我们采用云原生架构，**不使用nginx反向代理**，而是直接使用AWS Application Load Balancer：

```
Internet → ALB (路径路由) → {
  /api/* → Backend ECS Service (Port 8000)
  /*     → Frontend ECS Service (Port 3000)
}
```

**为什么不用nginx？**
- ✅ AWS ALB已提供负载均衡和路径路由
- ✅ 减少一层不必要的网络跳跃
- ✅ 降低运维复杂性和成本
- ✅ 更好的AWS生态集成（WAF、Certificate Manager等）
- ✅ 原生支持健康检查和自动故障转移

## 📋 前置要求

### AWS 资源准备

1. **AWS Account** 
2. **AWS CLI** 已安装并配置
3. **ECR Repositories** (将通过命令创建)
4. **ECS Cluster** (Fargate)
5. **Application Load Balancer**
6. **VPC & Subnets** (至少2个Public Subnets)
7. **Security Groups**
8. **EFS** (用于持久化存储)

## 🚀 部署步骤

### 第一步：AWS 基础设施设置

#### 1. 创建ECR repositories
```bash
# 创建前端ECR仓库
aws ecr create-repository \
    --repository-name excelsync-frontend \
    --image-scanning-configuration scanOnPush=true \
    --region us-west-2

# 创建后端ECR仓库  
aws ecr create-repository \
    --repository-name excelsync-backend \
    --image-scanning-configuration scanOnPush=true \
    --region us-west-2
```

#### 2. 创建ECS Cluster
```bash
aws ecs create-cluster \
    --cluster-name excelsync-cluster \
    --capacity-providers FARGATE \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1
```

#### 3. 创建CloudWatch Log Groups
```bash
aws logs create-log-group --log-group-name /ecs/excelsync-frontend
aws logs create-log-group --log-group-name /ecs/excelsync-backend
```

#### 4. 创建EFS文件系统（用于后端文件持久化）
```bash
aws efs create-file-system \
    --performance-mode generalPurpose \
    --throughput-mode provisioned \
    --provisioned-throughput-in-mibps 125 \
    --tags Key=Name,Value=excelsync-efs
```

#### 5. 创建IAM角色

**任务执行角色 (ecsTaskExecutionRole):**
```bash
# 创建信任策略文件
cat > ecs-task-execution-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# 创建角色
aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://ecs-task-execution-trust-policy.json

# 附加托管策略
aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### 第二步：GitHub Secrets 配置

在GitHub仓库Settings > Secrets and variables > Actions中添加：

| Secret Name | Value | Description |
|------------|-------|-------------|
| `AWS_ACCESS_KEY_ID` | 你的AWS访问密钥ID | IAM用户访问密钥 |
| `AWS_SECRET_ACCESS_KEY` | 你的AWS秘密访问密钥 | IAM用户秘密密钥 |

### 第三步：更新配置文件

#### 1. 更新任务定义模板

编辑 `ecs-task-definitions/frontend-task-definition.json`:
- 替换 `ACCOUNT_ID` 为你的AWS账户ID
- 替换 `REGION` 为你的AWS区域
- 更新 `NEXT_PUBLIC_API_URL` 为后端ALB的DNS名称

编辑 `ecs-task-definitions/backend-task-definition.json`:
- 替换 `ACCOUNT_ID` 为你的AWS账户ID  
- 替换 `REGION` 为你的AWS区域
- 替换 `fs-XXXXXXXXX` 为你的EFS文件系统ID

#### 2. 创建初始任务定义
```bash
aws ecs register-task-definition \
    --cli-input-json file://ecs-task-definitions/frontend-task-definition.json

aws ecs register-task-definition \
    --cli-input-json file://ecs-task-definitions/backend-task-definition.json
```

### 第四步：创建Application Load Balancer

#### 1. 创建ALB和目标组
```bash
# 创建前端目标组
aws elbv2 create-target-group \
    --name excelsync-frontend-tg \
    --protocol HTTP \
    --port 3000 \
    --vpc-id vpc-xxxxxxxx \
    --health-check-path / \
    --health-check-interval-seconds 30

# 创建后端目标组  
aws elbv2 create-target-group \
    --name excelsync-backend-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxxxxxxx \
    --health-check-path /api/health \
    --health-check-interval-seconds 30

# 创建Application Load Balancer
aws elbv2 create-load-balancer \
    --name excelsync-alb \
    --subnets subnet-xxxxxxxx subnet-yyyyyyyy \
    --security-groups sg-xxxxxxxx
```

#### 2. 配置ALB路由规则
```bash
# 创建监听器
aws elbv2 create-listener \
    --load-balancer-arn arn:aws:elasticloadbalancing:region:account:loadbalancer/app/excelsync-alb/xxxxxxxx \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:region:account:targetgroup/excelsync-frontend-tg/xxxxxxxx

# 添加API路径规则 (后端)
aws elbv2 create-rule \
    --listener-arn arn:aws:elasticloadbalancing:region:account:listener/app/excelsync-alb/xxxxxxxx/xxxxxxxx \
    --priority 100 \
    --conditions Field=path-pattern,Values="/api/*" \
    --actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:region:account:targetgroup/excelsync-backend-tg/xxxxxxxx
```

### 第五步：创建ECS服务

**前端服务配置：**
- 服务名称: `excelsync-frontend-service`
- 任务定义: `excelsync-frontend-task:1`
- 平台版本: LATEST
- 所需任务数: 2
- 子网: Private subnets (推荐)
- 安全组: 只允许ALB访问端口3000
- 负载均衡器: 关联到 excelsync-frontend-tg

**后端服务配置：**
- 服务名称: `excelsync-backend-service`
- 任务定义: `excelsync-backend-task:1`  
- 平台版本: LATEST
- 所需任务数: 2
- 子网: Private subnets (推荐)
- 安全组: 只允许ALB访问端口8000
- 负载均衡器: 关联到 excelsync-backend-tg

### 第六步：测试部署

1. **推送代码触发CI/CD**:
```bash
git add .
git commit -m "🚀 Setup ECS deployment"
git push origin main
```

2. **监控部署状态**:
- GitHub Actions界面查看构建状态
- AWS ECS控制台查看服务状态
- CloudWatch查看应用日志

3. **访问应用** (通过单一ALB入口):
- 前端: http://your-alb-dns/
- 后端API: http://your-alb-dns/api/health
- **路径路由**: ALB自动将 `/api/*` 请求转发到后端，其他请求转发到前端

## 🔍 故障排除

### 常见问题

1. **任务启动失败**
   - 检查CloudWatch日志
   - 验证ECR镜像是否成功推送
   - 确认IAM角色权限

2. **健康检查失败**
   - 检查安全组规则
   - 验证应用启动时间
   - 调整健康检查参数

3. **服务无法访问**
   - 检查负载均衡器配置
   - 验证目标组健康状态
   - 确认DNS解析

### 监控和日志

**CloudWatch指标:**
- CPU使用率
- 内存使用率
- 请求计数
- 错误率

**日志位置:**
- 前端: `/ecs/excelsync-frontend`
- 后端: `/ecs/excelsync-backend`

## 🔧 生产环境优化

### 性能优化
1. **启用Auto Scaling**
2. **配置CloudFront CDN**
3. **实现数据库缓存（Redis）**
4. **优化Docker镜像大小**

### 安全加固
1. **启用WAF**  
2. **配置SSL/TLS证书**
3. **实现密钥管理（Secrets Manager）**
4. **网络分段（Private Subnets）**

### 成本优化
1. **使用Spot容量**
2. **配置合适的CPU/内存规格**
3. **监控资源使用率**
4. **设置预算告警**

## 📚 相关文档

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## 🆘 支持

如果遇到问题，请检查：
1. GitHub Actions运行日志
2. AWS CloudWatch日志  
3. ECS服务事件
4. 创建Issue在GitHub仓库中