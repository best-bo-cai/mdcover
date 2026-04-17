import { Button, Space } from 'antd'

const ToolBar = ({ loadingType, onExportHtml, onExportPdf, onExportWord }) => {
  return (
    <Space wrap>
      <Button type="default" loading={loadingType === 'html'} onClick={onExportHtml}>
        导出 HTML
      </Button>
      <Button type="primary" loading={loadingType === 'pdf'} onClick={onExportPdf}>
        导出 PDF
      </Button>
      <Button type="dashed" loading={loadingType === 'word'} onClick={onExportWord}>
        导出 Word
      </Button>
    </Space>
  )
}

export default ToolBar
