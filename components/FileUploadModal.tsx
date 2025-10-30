
import React, { useCallback, useState, useEffect } from 'react';
import { DocumentType, Shipment } from '../types';
import { DOCUMENT_TYPES } from '../constants';
import { UploadIcon } from './icons/UploadIcon';
import { XCircleIcon } from './icons/XCircleIcon';

interface FileUploadModalProps {
    isOpen: boolean;
    onClose: () => void;
    onFileUpload: (file: File, shipmentId: string, docType: DocumentType, comments?: string) => void;
    shipmentId?: string;
    docType?: DocumentType;
    initialFile?: File;
    isAnalyzing: boolean;
    error: string | null;
    shipments: Shipment[];
}

const FileUploadModal: React.FC<FileUploadModalProps> = ({
    isOpen,
    onClose,
    onFileUpload,
    shipmentId: initialShipmentId,
    docType: initialDocType,
    initialFile,
    isAnalyzing,
    error,
    shipments
}) => {
    const [dragActive, setDragActive] = useState(false);
    const [file, setFile] = useState<File | null>(initialFile || null);
    const [selectedShipment, setSelectedShipment] = useState(initialShipmentId || '');
    const [selectedDocType, setSelectedDocType] = useState(initialDocType || '');
    const [comments, setComments] = useState('');

    useEffect(() => {
        setFile(initialFile || null);
        setSelectedShipment(initialShipmentId || '');
        setSelectedDocType(initialDocType || '');
        setComments('');
    }, [isOpen, initialFile, initialShipmentId, initialDocType]);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
        else if (e.type === "dragleave") setDragActive(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files?.[0]) setFile(e.dataTransfer.files[0]);
    };
    
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files?.[0]) setFile(e.target.files[0]);
    };
    
    const handleSubmit = () => {
        if (file && selectedShipment && selectedDocType) {
            onFileUpload(file, selectedShipment, selectedDocType as DocumentType, comments);
        }
    };

    const handleCancel = () => {
        setFile(null);
        onClose();
    }

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50 transition-opacity" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div className="bg-white rounded-lg shadow-xl transform transition-all sm:my-8 sm:max-w-2xl sm:w-full">
                <div className="p-6">
                    <div className="flex items-start">
                        <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-violet-100 sm:mx-0 sm:h-10 sm:w-10">
                            <UploadIcon className="h-6 w-6 text-violet-600"/>
                        </div>
                        <div className="mt-0 ml-4 text-left w-full">
                            <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-title">Upload Document</h3>
                            <p className="text-sm text-gray-500 mt-1">Attach a document and link it to a shipment.</p>
                        </div>
                    </div>

                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Left Side - File Upload */}
                        <div className="space-y-4">
                            {!file ? (
                                <label htmlFor="file-upload" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}
                                       className={`flex flex-col justify-center items-center w-full h-full px-6 py-10 border-2 ${dragActive ? 'border-violet-500' : 'border-gray-300'} border-dashed rounded-md cursor-pointer transition-colors duration-200`}>
                                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12h3m-1.5-1.5v3" />
                                    </svg>
                                    <span className="mt-2 block text-sm font-medium text-violet-600 hover:text-violet-500">Click to upload a file</span>
                                    <span className="mt-1 block text-xs text-gray-500">or drag and drop</span>
                                    <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleChange} />
                                </label>
                            ) : (
                                <div className="p-4 bg-gray-50 rounded-md border border-gray-200 text-sm h-full flex flex-col justify-center">
                                    <div className="flex justify-between items-center">
                                        <span className="font-medium text-gray-800 truncate">{file.name}</span>
                                        <button onClick={() => setFile(null)} className="text-gray-400 hover:text-gray-600"><XCircleIcon className="w-5 h-5"/></button>
                                    </div>
                                    <p className="text-xs text-gray-500 mt-1">{(file.size / 1024).toFixed(2)} KB</p>
                                </div>
                            )}
                        </div>

                        {/* Right Side - Form */}
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="shipment" className="block text-sm font-medium text-gray-700">Shipment (Invoice #)</label>
                                <select id="shipment" name="shipment" value={selectedShipment} onChange={(e) => setSelectedShipment(e.target.value)} disabled={!!initialShipmentId}
                                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-violet-500 focus:border-violet-500 sm:text-sm rounded-md disabled:bg-gray-100 disabled:cursor-not-allowed">
                                    <option value="">Select a shipment</option>
                                    {shipments.map(s => <option key={s.id} value={s.id}>{s.invoiceNumber}</option>)}
                                </select>
                            </div>
                            <div>
                                <label htmlFor="docType" className="block text-sm font-medium text-gray-700">Document Type</label>
                                <select id="docType" name="docType" value={selectedDocType} onChange={(e) => setSelectedDocType(e.target.value)} disabled={!!initialDocType}
                                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-violet-500 focus:border-violet-500 sm:text-sm rounded-md disabled:bg-gray-100 disabled:cursor-not-allowed">
                                    <option value="">Select a document type</option>
                                    {DOCUMENT_TYPES.map(d => <option key={d} value={d}>{d}</option>)}
                                </select>
                            </div>
                             <div>
                                <label htmlFor="comments" className="block text-sm font-medium text-gray-700">Comments (Optional)</label>
                                <textarea id="comments" name="comments" rows={3} value={comments} onChange={(e) => setComments(e.target.value)}
                                        className="mt-1 shadow-sm focus:ring-violet-500 focus:border-violet-500 block w-full sm:text-sm border border-gray-300 rounded-md"></textarea>
                            </div>
                        </div>
                    </div>
                     
                    {isAnalyzing && (
                        <div className="mt-4 flex items-center justify-center p-3">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-violet-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            <p className="text-sm text-gray-600 font-medium">Analyzing document with AI... Please wait.</p>
                        </div>
                    )}
                    {error && (
                         <div className="mt-4 p-3 bg-red-50 border border-red-200 text-sm text-red-700 rounded-md">
                             <p><span className="font-semibold">Error:</span> {error}</p>
                         </div>
                    )}
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded-b-lg">
                    <button type="button" onClick={handleSubmit} disabled={!file || !selectedShipment || !selectedDocType || isAnalyzing}
                            className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-violet-600 text-base font-medium text-white hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 sm:ml-3 sm:w-auto sm:text-sm disabled:bg-violet-300 disabled:cursor-not-allowed">
                        {isAnalyzing ? 'Analyzing...' : 'Upload & Analyze'}
                    </button>
                    <button type="button" onClick={handleCancel} disabled={isAnalyzing}
                            className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:w-auto sm:text-sm disabled:opacity-50">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FileUploadModal;
