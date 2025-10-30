
import React, { useState, useCallback, useMemo, useEffect } from 'react';
import { DocumentStatus, DocumentType, Shipment, UploadLogEntry, AnalyzedData, ModalState } from './types';
import { INITIAL_SHIPMENTS, DOCUMENT_TYPES } from './constants';
import { analyzeDocumentContent } from './services/geminiService';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import FileUploadModal from './components/FileUploadModal';
import AnalyticsOverview from './components/AnalyticsOverview';
import UploadLogs from './components/UploadLogs';

const App: React.FC = () => {
    const [shipments, setShipments] = useState<Shipment[]>(INITIAL_SHIPMENTS);
    const [uploadLogs, setUploadLogs] = useState<UploadLogEntry[]>([]);
    const [analyzedData, setAnalyzedData] = useState<AnalyzedData[]>([]);
    const [modalState, setModalState] = useState<ModalState>({ isOpen: false });
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [dragActive, setDragActive] = useState(false);

    const handleOpenModal = useCallback((shipmentId?: string, docType?: DocumentType, file?: File) => {
        setModalState({ isOpen: true, shipmentId, docType, file });
    }, []);

    const handleCloseModal = useCallback(() => {
        setModalState({ isOpen: false });
        setError(null);
    }, []);

    const handleFileUpload = useCallback(async (file: File, shipmentId: string, docType: DocumentType, comments?: string) => {
        setIsAnalyzing(true);
        setError(null);

        setShipments(prev => prev.map(shipment =>
            shipment.id === shipmentId ? {
                ...shipment,
                documents: {
                    ...shipment.documents,
                    [docType]: {
                        ...shipment.documents[docType],
                        status: DocumentStatus.PROCESSING
                    }
                }
            } : shipment
        ));

        try {
            // In a real app, you'd use a library like PDF.js or an OCR service to extract text.
            // For this demo, we'll send a structured placeholder to the AI.
            const fileContent = `--- DUMMY FILE CONTENT ---
            File Name: ${file.name}
            File Type: ${file.type}
            Size: ${file.size} bytes
            Document Type: ${docType}
            Shipment ID: ${shipmentId}
            This is a placeholder for the actual file content.
            --- END DUMMY CONTENT ---`;

            const analysisResult = await analyzeDocumentContent(fileContent, docType);

            setShipments(prev => prev.map(shipment =>
                shipment.id === shipmentId ? {
                    ...shipment,
                    documents: {
                        ...shipment.documents,
                        [docType]: {
                            name: file.name,
                            status: DocumentStatus.UPLOADED,
                            uploadDate: new Date().toISOString(),
                            uploader: 'Admin User',
                            driveLink: `https://mock-drive.com/${shipment.invoiceNumber}/${file.name}`,
                            analysisSummary: analysisResult.analysisSummary,
                        }
                    },
                    ...analysisResult.invoiceNumber && { invoiceNumber: analysisResult.invoiceNumber }
                } : shipment
            ));

            const newLog: UploadLogEntry = {
                id: `log-${Date.now()}`,
                fileName: file.name,
                driveLink: `https://mock-drive.com/${shipmentId}/${file.name}`,
                uploadTimestamp: new Date().toISOString(),
                documentType: docType,
                uploader: 'Admin User',
                shipmentId: shipmentId,
                analysisStatus: 'Success',
                comments,
                extractedData: analysisResult
            };
            setUploadLogs(prev => [newLog, ...prev]);

            if (analysisResult) {
                setAnalyzedData(prev => [...prev, { shipmentId, ...analysisResult }]);
            }

            handleCloseModal();

        } catch (err) {
            console.error("Analysis failed:", err);
            setError("Failed to analyze document. The content might be invalid or the service is unavailable. Please try again.");
            setShipments(prev => prev.map(shipment =>
                shipment.id === shipmentId ? {
                    ...shipment,
                    documents: {
                        ...shipment.documents,
                        [docType]: {
                            ...shipment.documents[docType],
                            status: DocumentStatus.ERROR
                        }
                    }
                } : shipment
            ));
        } finally {
            setIsAnalyzing(false);
        }
    }, [handleCloseModal]);
    
    const analyticsSummary = useMemo(() => {
        const totalDocs = shipments.length * DOCUMENT_TYPES.length;
        const uploadedDocs = shipments.flatMap(s => Object.values(s.documents)).filter(d => d.status === DocumentStatus.UPLOADED).length;
        const missingDocs = totalDocs - uploadedDocs;
        const totalValue = analyzedData.reduce((sum, data) => sum + (data.totalAmount || 0), 0);
        return { totalDocs, uploadedDocs, missingDocs, totalValue };
    }, [shipments, analyzedData]);

    // Drag and drop handlers
    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }, []);
    
    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
           handleOpenModal(undefined, undefined, e.dataTransfer.files[0]);
        }
    }, [handleOpenModal]);

    return (
        <div className="min-h-screen bg-gray-100" onDragEnter={handleDrag}>
            <Header onUploadClick={() => handleOpenModal()} />
            <main className="p-4 sm:p-6 lg:p-8">
                <AnalyticsOverview summary={analyticsSummary} />
                <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2">
                        <Dashboard shipments={shipments} />
                    </div>
                    <div className="lg:col-span-1">
                        <UploadLogs logs={uploadLogs} shipments={shipments} />
                    </div>
                </div>
            </main>
            {dragActive && (
                <div
                    className="fixed inset-0 bg-gray-900 bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center"
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <div className="pointer-events-none flex flex-col items-center text-white">
                        <svg className="w-24 h-24 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                           <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l-3.75 3.75M12 9.75l3.75 3.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-2xl font-bold">Drop file to upload</p>
                    </div>
                </div>
            )}
            {modalState.isOpen && (
                <FileUploadModal
                    isOpen={modalState.isOpen}
                    onClose={handleCloseModal}
                    onFileUpload={handleFileUpload}
                    shipmentId={modalState.shipmentId}
                    docType={modalState.docType}
                    initialFile={modalState.file}
                    isAnalyzing={isAnalyzing}
                    error={error}
                    shipments={shipments}
                />
            )}
        </div>
    );
};

export default App;
