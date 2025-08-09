from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
import traceback
from pathlib import Path

# 导入我们的处理器
from md_parser import MDParser
from md_to_excel_processor import MDToExcelProcessor

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 添加请求日志中间件
@app.before_request
def log_request_info():
    logger.info('=== 新请求开始 ===')
    logger.info(f'请求方法: {request.method}')
    logger.info(f'请求路径: {request.path}')
    logger.info(f'请求来源: {request.remote_addr}')
    if request.args:
        logger.info(f'URL参数: {dict(request.args)}')
    if request.form:
        logger.info(f'表单数据: {dict(request.form)}')
    if request.files:
        logger.info(f'上传文件: {list(request.files.keys())}')

# 配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'md', 'markdown', 'txt'}

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    logger.info("💓 健康检查请求")
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/parse-md', methods=['POST'])
def parse_md_file():
    """解析单个MD文件接口"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # 检查文件名
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only .md, .markdown, and .txt files are allowed'
            }), 400
        
        # 读取文件内容
        content = file.read().decode('utf-8')
        
        # 使用MDParser解析内容
        parser = MDParser()
        result = parser.parse(content)
        
        # 返回解析结果
        return jsonify({
            'success': True,
            'data': {
                'headers': result.get('headers', []),
                'data': result.get('rows', []),
                'summary': {
                    'totalRows': len(result.get('rows', [])),
                    'totalColumns': len(result.get('headers', [])),
                    'fileName': secure_filename(file.filename),
                    'fileSize': len(content),
                    'parsedAt': datetime.now().isoformat()
                },
                'metadata': result.get('metadata', {})
            }
        })
        
    except UnicodeDecodeError:
        return jsonify({
            'success': False,
            'error': 'File encoding error. Please ensure the file is UTF-8 encoded'
        }), 400
        
    except Exception as e:
        app.logger.error(f"Error parsing MD file: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Failed to parse file: {str(e)}'
        }), 500

@app.route('/api/parse-multiple-md', methods=['POST'])
def parse_multiple_md_files():
    """批量解析MD文件接口"""
    try:
        files = request.files.getlist('files')
        
        if not files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            }), 400
        
        results = []
        errors = []
        
        for idx, file in enumerate(files):
            try:
                if not allowed_file(file.filename):
                    errors.append({
                        'file': file.filename,
                        'error': 'Invalid file type'
                    })
                    continue
                
                # 读取文件内容
                content = file.read().decode('utf-8')
                
                # 使用MDParser解析内容
                parser = MDParser()
                result = parser.parse(content)
                
                # 添加到结果列表
                results.append({
                    'headers': result.get('headers', []),
                    'data': result.get('rows', []),
                    'summary': {
                        'totalRows': len(result.get('rows', [])),
                        'totalColumns': len(result.get('headers', [])),
                        'fileName': secure_filename(file.filename),
                        'fileSize': len(content),
                        'parsedAt': datetime.now().isoformat()
                    },
                    'metadata': result.get('metadata', {})
                })
                
            except Exception as e:
                errors.append({
                    'file': file.filename,
                    'error': str(e)
                })
        
        return jsonify({
            'success': len(results) > 0,
            'data': results,
            'errors': errors if errors else None,
            'summary': {
                'totalFiles': len(files),
                'successCount': len(results),
                'errorCount': len(errors)
            }
        })
        
    except Exception as e:
        app.logger.error(f"Error parsing multiple MD files: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to parse files: {str(e)}'
        }), 500

@app.route('/api/parse-md-text', methods=['POST'])
def parse_md_text():
    """解析MD文本内容接口（不需要文件上传）"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'No content provided'
            }), 400
        
        content = data['content']
        filename = data.get('filename', 'untitled.md')
        
        # 使用MDParser解析内容
        parser = MDParser()
        result = parser.parse(content)
        
        # 返回解析结果
        return jsonify({
            'success': True,
            'data': {
                'headers': result.get('headers', []),
                'data': result.get('rows', []),
                'summary': {
                    'totalRows': len(result.get('rows', [])),
                    'totalColumns': len(result.get('headers', [])),
                    'fileName': filename,
                    'fileSize': len(content),
                    'parsedAt': datetime.now().isoformat()
                },
                'metadata': result.get('metadata', {})
            }
        })
        
    except Exception as e:
        app.logger.error(f"Error parsing MD text: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to parse content: {str(e)}'
        }), 500

@app.route('/api/sample-md', methods=['GET'])
def get_sample_md():
    """获取示例MD文件内容"""
    sample_content = """# 资产负债表

| 科目 | 金额 |
|------|------|
| 现金 | 1000000 |
| 银行存款 | 5000000 |
| 应收账款 | 2000000 |
| 库存商品 | 3000000 |
| 流动资产合计 | 11000000 |
| 建筑物 | 8000000 |
| 机械设备 | 2000000 |
| 固定资产合计 | 10000000 |
| 总资产 | 21000000 |
"""
    
    return jsonify({
        'success': True,
        'content': sample_content,
        'filename': 'sample_balance_sheet.md'
    })

@app.route('/api/generate-excel', methods=['POST'])
def generate_excel_from_md():
    """从MD文件生成Excel文件（支持多文件）"""
    logger.info("🚀 开始处理Excel生成请求 (文件上传方式)")
    try:
        # 检查是否有文件（支持单文件和多文件）
        files = []
        if 'file' in request.files:
            files = [request.files['file']]
        elif 'files' in request.files:
            files = request.files.getlist('files')
        else:
            logger.error("❌ 请求中没有文件")
            return jsonify({
                'success': False,
                'error': 'No file provided',
                'error_code': 'NO_FILE'
            }), 400
        
        logger.info(f"📁 接收到 {len(files)} 个文件")
        
        results = []
        errors = []
        
        for idx, file in enumerate(files):
            try:
                logger.info(f"📄 处理文件 {idx + 1}/{len(files)}: {file.filename}")
                
                # 检查文件名
                if file.filename == '':
                    errors.append({
                        'filename': f'file_{idx + 1}',
                        'error': 'No file selected',
                        'error_code': 'EMPTY_FILENAME'
                    })
                    continue
                
                # 检查文件类型
                if not allowed_file(file.filename):
                    errors.append({
                        'filename': file.filename,
                        'error': f'Invalid file type. Only .md, .markdown, and .txt files are allowed',
                        'error_code': 'INVALID_FILE_TYPE'
                    })
                    continue
                
                # 读取文件内容
                content = file.read().decode('utf-8')
                logger.info(f"📖 文件内容长度: {len(content)} 字符")
                
                # 使用MD到Excel处理器
                processor = MDToExcelProcessor()
                result = processor.process_md_content(content, secure_filename(file.filename))
                
                if result['success']:
                    logger.info(f"✅ Excel生成成功: {result['output_filename']}")
                    results.append({
                        'filename': file.filename,
                        'output_filename': result['output_filename'],
                        'download_url': f"/api/download-excel/{result['output_filename']}",
                        'md_parsing': result['md_parsing'],
                        'excel_writing': result['excel_writing'],
                        'timestamp': result['timestamp']
                    })
                else:
                    logger.error(f"❌ Excel生成失败: {result.get('error', 'Unknown error')}")
                    errors.append({
                        'filename': file.filename,
                        'error': result.get('error', 'Unknown error occurred'),
                        'error_code': 'GENERATION_FAILED',
                        'stage': result.get('stage', 'unknown')
                    })
                    
            except UnicodeDecodeError:
                errors.append({
                    'filename': file.filename,
                    'error': 'File encoding error. Please ensure the file is UTF-8 encoded',
                    'error_code': 'ENCODING_ERROR'
                })
            except Exception as e:
                logger.error(f"💥 处理文件 {file.filename} 时发生异常: {str(e)}")
                errors.append({
                    'filename': file.filename,
                    'error': str(e),
                    'error_code': 'UNEXPECTED_ERROR'
                })
        
        # 返回综合结果
        success = len(results) > 0
        response_data = {
            'success': success,
            'data': {
                'results': results,
                'errors': errors if errors else [],
                'summary': {
                    'total_files': len(files),
                    'success_count': len(results),
                    'error_count': len(errors)
                }
            }
        }
        
        if not success and errors:
            response_data['error'] = 'All files failed to process'
            response_data['error_code'] = 'ALL_FAILED'
            
        return jsonify(response_data), 200 if success else 400
            
    except Exception as e:
        logger.error(f"💥 Excel生成过程中发生异常: {str(e)}")
        logger.error(f"💥 异常堆栈: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate Excel files: {str(e)}',
            'error_code': 'SERVER_ERROR'
        }), 500

@app.route('/api/generate-excel-text', methods=['POST'])
def generate_excel_from_md_text():
    """从MD文本内容生成Excel文件"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'No content provided'
            }), 400
        
        content = data['content']
        filename = data.get('filename', 'untitled.md')
        
        # 使用MD到Excel处理器
        processor = MDToExcelProcessor()
        result = processor.process_md_content(content, filename)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'output_filename': result['output_filename'],
                    'download_url': f"/api/download-excel/{result['output_filename']}",
                    'md_parsing': result['md_parsing'],
                    'excel_writing': result['excel_writing'],
                    'timestamp': result['timestamp']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred'),
                'stage': result.get('stage', 'unknown')
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error generating Excel from MD text: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate Excel file: {str(e)}'
        }), 500

@app.route('/api/download-excel/<filename>', methods=['GET'])
def download_excel_file(filename):
    """下载生成的Excel文件"""
    try:
        processor = MDToExcelProcessor()
        file_path = processor.get_output_file(filename)
        
        if not file_path or not Path(file_path).exists():
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        app.logger.error(f"Error downloading Excel file {filename}: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to download file: {str(e)}'
        }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)