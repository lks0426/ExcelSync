// Error code to user-friendly message mapping
export const errorMessages: Record<string, Record<string, string>> = {
  ja: {
    // Japanese (Default)
    NO_FILE: 'ファイルが選択されていません',
    EMPTY_FILENAME: 'ファイル名が空です',
    INVALID_FILE_TYPE: 'サポートされていないファイル形式です。.md、.markdown、.txt ファイルのみ対応しています',
    ENCODING_ERROR: 'ファイルのエンコーディングエラーです。UTF-8形式であることを確認してください',
    GENERATION_FAILED: 'Excelファイルの生成に失敗しました',
    UNEXPECTED_ERROR: '予期しないエラーが発生しました',
    SERVER_ERROR: 'サーバーエラーが発生しました',
    ALL_FAILED: 'すべてのファイルの処理に失敗しました',
    NO_VALID_FILES: '処理可能なファイルがありません',
    FILE_TOO_LARGE: 'ファイルサイズが大きすぎます（最大16MB）',
    NETWORK_ERROR: 'ネットワークエラーが発生しました',
    TIMEOUT_ERROR: 'タイムアウトエラーが発生しました',
    PARSE_ERROR: 'ファイルの解析に失敗しました',
    NO_TABLE_FOUND: '有効なテーブルが見つかりませんでした',
    DOWNLOAD_FAILED: 'ダウンロードに失敗しました',
    // Generic fallback
    UNKNOWN_ERROR: '不明なエラーが発生しました'
  },
  zh: {
    // Chinese
    NO_FILE: '未选择文件',
    EMPTY_FILENAME: '文件名为空',
    INVALID_FILE_TYPE: '不支持的文件格式。仅支持 .md、.markdown、.txt 文件',
    ENCODING_ERROR: '文件编码错误。请确保文件为UTF-8格式',
    GENERATION_FAILED: 'Excel文件生成失败',
    UNEXPECTED_ERROR: '发生意外错误',
    SERVER_ERROR: '服务器错误',
    ALL_FAILED: '所有文件处理失败',
    NO_VALID_FILES: '没有可处理的文件',
    FILE_TOO_LARGE: '文件过大（最大16MB）',
    NETWORK_ERROR: '网络错误',
    TIMEOUT_ERROR: '超时错误',
    PARSE_ERROR: '文件解析失败',
    NO_TABLE_FOUND: '未找到有效的表格',
    DOWNLOAD_FAILED: '下载失败',
    // Generic fallback
    UNKNOWN_ERROR: '未知错误'
  },
  en: {
    // English
    NO_FILE: 'No file selected',
    EMPTY_FILENAME: 'File name is empty',
    INVALID_FILE_TYPE: 'Unsupported file format. Only .md, .markdown, and .txt files are supported',
    ENCODING_ERROR: 'File encoding error. Please ensure the file is UTF-8 encoded',
    GENERATION_FAILED: 'Failed to generate Excel file',
    UNEXPECTED_ERROR: 'An unexpected error occurred',
    SERVER_ERROR: 'Server error occurred',
    ALL_FAILED: 'All files failed to process',
    NO_VALID_FILES: 'No valid files to process',
    FILE_TOO_LARGE: 'File too large (max 16MB)',
    NETWORK_ERROR: 'Network error occurred',
    TIMEOUT_ERROR: 'Request timeout',
    PARSE_ERROR: 'Failed to parse file',
    NO_TABLE_FOUND: 'No valid table found',
    DOWNLOAD_FAILED: 'Download failed',
    // Generic fallback
    UNKNOWN_ERROR: 'Unknown error occurred'
  }
}

export const getErrorMessage = (errorCode: string | undefined, language: string = 'ja', fallbackMessage?: string): string => {
  if (!errorCode) {
    return fallbackMessage || errorMessages[language].UNKNOWN_ERROR || 'Error occurred'
  }
  
  const messages = errorMessages[language] || errorMessages.ja
  return messages[errorCode] || fallbackMessage || messages.UNKNOWN_ERROR || errorCode
}

// Get detailed error info with suggestions
export const getErrorInfo = (errorCode: string | undefined, language: string = 'ja') => {
  const message = getErrorMessage(errorCode, language)
  
  const suggestions: Record<string, Record<string, string[]>> = {
    ja: {
      INVALID_FILE_TYPE: [
        'ファイル拡張子を確認してください',
        '.md、.markdown、.txt のいずれかである必要があります'
      ],
      ENCODING_ERROR: [
        'テキストエディタでファイルを開き、UTF-8形式で保存し直してください',
        'Windowsのメモ帳を使用している場合は、「名前を付けて保存」で文字コードをUTF-8に指定してください'
      ],
      NO_TABLE_FOUND: [
        'Markdownテーブル形式（|で区切られた表）またはHTMLテーブル（<table>タグ）が含まれているか確認してください',
        'テーブルの形式が正しいか確認してください'
      ],
      FILE_TOO_LARGE: [
        'ファイルサイズを16MB以下に縮小してください',
        '大きなファイルは分割して処理してください'
      ]
    },
    zh: {
      INVALID_FILE_TYPE: [
        '请检查文件扩展名',
        '必须是 .md、.markdown 或 .txt'
      ],
      ENCODING_ERROR: [
        '请用文本编辑器打开文件，并以UTF-8格式重新保存',
        '如果使用Windows记事本，请在"另存为"时指定编码为UTF-8'
      ],
      NO_TABLE_FOUND: [
        '请确认文件包含Markdown表格（用|分隔）或HTML表格（<table>标签）',
        '请检查表格格式是否正确'
      ],
      FILE_TOO_LARGE: [
        '请将文件大小缩小到16MB以下',
        '大文件请分割后处理'
      ]
    },
    en: {
      INVALID_FILE_TYPE: [
        'Please check the file extension',
        'Must be .md, .markdown, or .txt'
      ],
      ENCODING_ERROR: [
        'Please open the file in a text editor and save it as UTF-8',
        'If using Windows Notepad, specify UTF-8 encoding when saving'
      ],
      NO_TABLE_FOUND: [
        'Please ensure the file contains a Markdown table (separated by |) or HTML table (<table> tags)',
        'Please check if the table format is correct'
      ],
      FILE_TOO_LARGE: [
        'Please reduce the file size to under 16MB',
        'For large files, please split them for processing'
      ]
    }
  }
  
  const langSuggestions = suggestions[language] || suggestions.ja
  const errorSuggestions = (errorCode && langSuggestions[errorCode]) || []
  
  return {
    message,
    suggestions: errorSuggestions
  }
}