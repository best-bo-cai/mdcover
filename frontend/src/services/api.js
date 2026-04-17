import axios from 'axios'

const apiClient = axios.create({
  timeout: 120000,
})

const downloadBlob = (blob, fileName) => {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

const parseFilename = (disposition, fallback) => {
  if (!disposition) return fallback
  const match = disposition.match(/filename=\"?([^\";]+)\"?/)
  return match?.[1] || fallback
}

export const exportHtml = async (markdown) => {
  const response = await apiClient.post('/api/convert/html', { markdown })
  const blob = new Blob([response.data], { type: 'text/html;charset=utf-8' })
  const fileName = parseFilename(response.headers['content-disposition'], 'document.html')
  downloadBlob(blob, fileName)
}

export const exportPdf = async (markdown) => {
  const response = await apiClient.post('/api/convert/pdf', { markdown }, { responseType: 'blob' })
  const fileName = parseFilename(response.headers['content-disposition'], 'document.pdf')
  downloadBlob(response.data, fileName)
}

export const exportWord = async (markdown) => {
  const response = await apiClient.post('/api/convert/word', { markdown }, { responseType: 'blob' })
  const fileName = parseFilename(response.headers['content-disposition'], 'document.docx')
  downloadBlob(response.data, fileName)
}
