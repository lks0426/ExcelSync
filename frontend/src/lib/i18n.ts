// i18n configuration for Japanese, Chinese, and English
export const translations = {
  ja: {
    // Japanese (Default)
    app: {
      title: 'MarkdownSync',
      subtitle: 'モダンなMarkdownファイルアップロード＆テーブル解析ツール',
      uploadSection: 'アップロード＆解析',
      dataPreview: 'データプレビュー',
      noDataPreview: 'プレビューするデータがありません',
      noDataPreviewDesc: 'Markdownファイルをアップロードして解析すると、ここにデータが表示されます'
    },
    fileUpload: {
      dropActive: 'ここにファイルをドロップ',
      dropActiveDesc: 'Markdownファイルをリリースしてアップロード',
      uploadTitle: 'Markdownファイルをアップロード',
      uploadDesc: 'ここにMarkdownファイルをドラッグ＆ドロップするか、クリックして選択',
      uploadedFiles: 'アップロードされたファイル',
      fileStatus: {
        uploading: 'アップロード中',
        uploaded: 'アップロード完了',
        processing: '処理中',
        completed: '完了',
        error: 'エラー'
      }
    },
    parseButton: {
      generate: 'Excel生成',
      parsing: 'ファイル解析中...',
      success: '解析成功！',
      failed: '解析失敗',
      fileCount_one: '{{count}}ファイル',
      fileCount_other: '{{count}}ファイル'
    },
    dataPreview: {
      fileName: 'ファイル名',
      totalRows: '総行数',
      totalColumns: '総列数',
      parsedAt: '解析日時',
      downloadExcel: 'Excelダウンロード',
      downloadCSV: 'CSVダウンロード',
      excelInfo: 'Excel情報',
      outputFile: '出力ファイル',
      successRate: '成功率',
      totalFields: '総フィールド数',
      successfulWrites: '成功した書き込み',
      parsedData: '解析データ',
      files: 'ファイル',
      fileSize: 'ファイルサイズ',
      excelGenerated: 'Excelファイル生成完了',
      fieldsMapped: 'フィールドが正常にマッピングされました',
      fileNav: '{{current}} / {{total}} ファイル'
    },
    errors: {
      parseError: '解析エラー',
      networkError: 'ネットワークエラー',
      suggestions: '提案：'
    },
    features: {
      markdownTables: {
        title: 'Markdownテーブル',
        desc: 'MarkdownテーブルをJSONに解析'
      },
      fastProcessing: {
        title: '高速処理',
        desc: 'リアルタイム進捗表示での高速解析'
      },
      responsive: {
        title: 'レスポンシブ',
        desc: 'すべてのデバイスでシームレスに動作'
      },
      modernDesign: {
        title: 'モダンデザイン',
        desc: '美しいグラスモーフィズムインターフェース'
      }
    },
    status: {
      ready: '{{count}}ファイル準備完了',
      processing: '処理中...',
      completed: '完了',
      error: 'エラー'
    }
  },
  zh: {
    // Chinese
    app: {
      title: 'MarkdownSync',
      subtitle: '现代化Markdown文件上传和表格解析工具',
      uploadSection: '上传与解析',
      dataPreview: '数据预览',
      noDataPreview: '没有可预览的数据',
      noDataPreviewDesc: '上传并解析Markdown文件后，数据将在此显示'
    },
    fileUpload: {
      dropActive: '将文件拖放到此处',
      dropActiveDesc: '释放以上传Markdown文件',
      uploadTitle: '上传Markdown文件',
      uploadDesc: '拖放Markdown文件到此处，或点击选择文件',
      uploadedFiles: '已上传文件',
      fileStatus: {
        uploading: '上传中',
        uploaded: '已上传',
        processing: '处理中',
        completed: '已完成',
        error: '错误'
      }
    },
    parseButton: {
      generate: '生成Excel',
      parsing: '正在解析文件...',
      success: '解析成功！',
      failed: '解析失败',
      fileCount_one: '{{count}}个文件',
      fileCount_other: '{{count}}个文件'
    },
    dataPreview: {
      fileName: '文件名',
      totalRows: '总行数',
      totalColumns: '总列数',
      parsedAt: '解析时间',
      downloadExcel: '下载Excel',
      downloadCSV: '下载CSV',
      excelInfo: 'Excel信息',
      outputFile: '输出文件',
      successRate: '成功率',
      totalFields: '总字段数',
      successfulWrites: '成功写入',
      parsedData: '解析数据',
      files: '文件',
      fileSize: '文件大小',
      excelGenerated: 'Excel文件生成完成',
      fieldsMapped: '字段映射成功',
      fileNav: '第 {{current}} / {{total}} 个文件'
    },
    errors: {
      parseError: '解析错误',
      networkError: '网络错误',
      suggestions: '建议：'
    },
    features: {
      markdownTables: {
        title: 'Markdown表格',
        desc: '将Markdown表格解析为JSON'
      },
      fastProcessing: {
        title: '快速处理',
        desc: '实时进度显示的快速解析'
      },
      responsive: {
        title: '响应式设计',
        desc: '在所有设备上无缝运行'
      },
      modernDesign: {
        title: '现代设计',
        desc: '美观的玻璃态界面'
      }
    },
    status: {
      ready: '{{count}}个文件就绪',
      processing: '处理中...',
      completed: '已完成',
      error: '错误'
    }
  },
  en: {
    // English
    app: {
      title: 'MarkdownSync',
      subtitle: 'Modern Markdown file upload & table parsing tool',
      uploadSection: 'Upload & Parse',
      dataPreview: 'Data Preview',
      noDataPreview: 'No data to preview',
      noDataPreviewDesc: 'Upload and parse Markdown files to see the data preview here'
    },
    fileUpload: {
      dropActive: 'Drop your files here',
      dropActiveDesc: 'Release to upload Markdown files',
      uploadTitle: 'Upload Markdown Files',
      uploadDesc: 'Drag & drop your Markdown files here, or click to browse',
      uploadedFiles: 'Uploaded Files',
      fileStatus: {
        uploading: 'Uploading',
        uploaded: 'Uploaded',
        processing: 'Processing',
        completed: 'Completed',
        error: 'Error'
      }
    },
    parseButton: {
      generate: 'Generate Excel',
      parsing: 'Parsing Files...',
      success: 'Parsed Successfully!',
      failed: 'Parsing Failed',
      fileCount_one: '{{count}} file',
      fileCount_other: '{{count}} files'
    },
    dataPreview: {
      fileName: 'File Name',
      totalRows: 'Total Rows',
      totalColumns: 'Total Columns',
      parsedAt: 'Parsed At',
      downloadExcel: 'Download Excel',
      downloadCSV: 'Download CSV',
      excelInfo: 'Excel Info',
      outputFile: 'Output File',
      successRate: 'Success Rate',
      totalFields: 'Total Fields',
      successfulWrites: 'Successful Writes',
      parsedData: 'Parsed Data',
      files: 'files',
      fileSize: 'File Size',
      excelGenerated: 'Excel File Generated',
      fieldsMapped: 'fields mapped successfully',
      fileNav: 'File {{current}} of {{total}}'
    },
    errors: {
      parseError: 'Parse Error',
      networkError: 'Network Error',
      suggestions: 'Suggestions:'
    },
    features: {
      markdownTables: {
        title: 'Markdown Tables',
        desc: 'Parse Markdown table syntax to JSON'
      },
      fastProcessing: {
        title: 'Fast Processing',
        desc: 'Quick parsing with real-time progress'
      },
      responsive: {
        title: 'Responsive',
        desc: 'Works seamlessly on all devices'
      },
      modernDesign: {
        title: 'Modern Design',
        desc: 'Beautiful glassmorphism interface'
      }
    },
    status: {
      ready: '{{count}} file ready',
      ready_plural: '{{count}} files ready',
      processing: 'Processing...',
      completed: 'Completed',
      error: 'Error'
    }
  }
}

export type Language = keyof typeof translations
export type TranslationKey = string

// Get translation with fallback
export const t = (key: string, language: Language = 'ja', params?: Record<string, any>): string => {
  const keys = key.split('.')
  let value: any = translations[language] || translations.ja
  
  for (const k of keys) {
    value = value?.[k]
    if (!value) break
  }
  
  if (typeof value !== 'string') {
    // Fallback to Japanese if translation not found
    value = translations.ja
    for (const k of keys) {
      value = value?.[k]
      if (!value) break
    }
  }
  
  if (typeof value !== 'string') {
    return key // Return key if translation not found
  }
  
  // Replace parameters
  if (params) {
    Object.entries(params).forEach(([param, val]) => {
      value = value.replace(new RegExp(`{{${param}}}`, 'g'), String(val))
    })
  }
  
  return value
}

// Language names for display
export const languageNames: Record<Language, string> = {
  ja: '日本語',
  zh: '中文',
  en: 'English'
}

// Get browser language with fallback to Japanese
export const getBrowserLanguage = (): Language => {
  if (typeof window === 'undefined') return 'ja'
  
  const browserLang = navigator.language.toLowerCase()
  
  if (browserLang.startsWith('ja')) return 'ja'
  if (browserLang.startsWith('zh')) return 'zh'
  if (browserLang.startsWith('en')) return 'en'
  
  return 'ja' // Default to Japanese
}