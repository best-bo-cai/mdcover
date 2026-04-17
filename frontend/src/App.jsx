import { useState } from 'react'
import { Alert, Layout, Typography, message } from 'antd'

import MdEditor from './components/MdEditor'
import ToolBar from './components/ToolBar'
import { exportHtml, exportPdf, exportWord } from './services/api'

const { Header, Content } = Layout

const initialMarkdown = `# Markdown Converter\n\n这是一个示例文档。\n\n## 表格\n\n| Name | Value |\n| --- | --- |\n| A | 1 |\n| B | 2 |\n\n## 代码\n\n\`\`\`python\ndef hello(name: str) -> str:\n    return f"Hello, {name}"\n\`\`\``

function App() {
  const [markdown, setMarkdown] = useState(initialMarkdown)
  const [loadingType, setLoadingType] = useState('')
  const [messageApi, contextHolder] = message.useMessage()

  const withExport = async (type, handler) => {
    if (!markdown.trim()) {
      messageApi.error('Markdown 不能为空')
      return
    }

    try {
      setLoadingType(type)
      await handler(markdown)
      messageApi.success('导出成功')
    } catch (error) {
      const detail = error?.response?.data?.detail
      messageApi.error(detail || '导出失败，请检查后端服务')
    } finally {
      setLoadingType('')
    }
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {contextHolder}
      <Header
        style={{
          background: '#fff',
          borderBottom: '1px solid #f0f0f0',
          paddingInline: 20,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Typography.Title level={4} style={{ margin: 0 }}>
          Markdown Converter (MVP)
        </Typography.Title>
        <ToolBar
          loadingType={loadingType}
          onExportHtml={() => withExport('html', exportHtml)}
          onExportPdf={() => withExport('pdf', exportPdf)}
          onExportWord={() => withExport('word', exportWord)}
        />
      </Header>

      <Content style={{ padding: 20 }}>
        <Alert
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
          message="前端仅负责编辑与预览，所有导出由后端完成。"
        />
        <MdEditor value={markdown} onChange={setMarkdown} />
      </Content>
    </Layout>
  )
}

export default App
