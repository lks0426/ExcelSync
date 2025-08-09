// 测试API导入
const { api } = require('./src/lib/api.ts')

console.log('API methods available:')
console.log('- generateExcel:', typeof api.generateExcel)
console.log('- generateExcelFromText:', typeof api.generateExcelFromText)
console.log('- downloadExcel:', typeof api.downloadExcel)
console.log('- getSampleMD:', typeof api.getSampleMD)
console.log('- healthCheck:', typeof api.healthCheck)

if (typeof api.generateExcel !== 'function') {
  console.error('❌ generateExcel method is missing!')
} else {
  console.log('✅ All API methods are available')
}