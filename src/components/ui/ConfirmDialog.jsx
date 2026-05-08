import Modal from './Modal'

export default function ConfirmDialog({ message, onConfirm, onCancel }) {
  return (
    <Modal title="Confirmar acción" onClose={onCancel}>
      <p className="text-gray-600 text-sm mb-5">{message}</p>
      <div className="flex justify-end gap-2">
        <button onClick={onCancel} className="px-4 py-2 text-sm rounded-lg border border-gray-200 hover:bg-gray-50">
          Cancelar
        </button>
        <button onClick={onConfirm} className="px-4 py-2 text-sm rounded-lg bg-red-500 text-white hover:bg-red-600">
          Eliminar
        </button>
      </div>
    </Modal>
  )
}
