import MDEditor from '@uiw/react-md-editor'

const MdEditor = ({ value, onChange }) => {
  return (
    <MDEditor
      height={680}
      value={value}
      onChange={(next) => onChange(next ?? '')}
      preview="live"
      visibleDragbar={false}
    />
  )
}

export default MdEditor
