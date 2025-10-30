
import React from 'react';
import { DocumentStatus } from '../types';
import { CheckCircleIcon } from './icons/CheckCircleIcon';
import { XCircleIcon } from './icons/XCircleIcon';
import { ExclamationCircleIcon } from './icons/ExclamationCircleIcon';
import { DocumentDuplicateIcon } from './icons/DocumentDuplicateIcon';

interface DocumentStatusCellProps {
    document: {
        status: DocumentStatus;
        name?: string;
        analysisSummary?: string;
    };
}

const DocumentStatusCell: React.FC<DocumentStatusCellProps> = ({ document }) => {

    const getStatusIndicator = () => {
        switch (document.status) {
            case DocumentStatus.UPLOADED:
                return (
                    <div className="relative group flex flex-col items-center text-green-600 cursor-pointer">
                        <CheckCircleIcon className="w-6 h-6" />
                        <span className="text-xs mt-1 font-medium">{document.status}</span>
                         {document.analysisSummary && (
                            <div className="absolute bottom-full mb-2 w-72 p-3 bg-gray-800 text-white text-xs rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 pointer-events-none">
                                <p className="font-bold border-b border-gray-600 pb-1 mb-1 truncate">{document.name}</p>
                                <p className="font-normal">{document.analysisSummary}</p>
                                <div className="absolute left-1/2 transform -translate-x-1/2 top-full w-0 h-0 border-x-8 border-x-transparent border-t-8 border-t-gray-800"></div>
                            </div>
                        )}
                    </div>
                );
            case DocumentStatus.MISSING:
                return (
                    <div className="flex flex-col items-center text-gray-400">
                       <ExclamationCircleIcon className="w-6 h-6"/>
                       <span className="text-xs mt-1 font-medium">{document.status}</span>
                    </div>
                );
            case DocumentStatus.PROCESSING:
                return (
                    <div className="flex flex-col items-center text-blue-500 animate-pulse">
                         <svg className="animate-spin h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span className="text-xs mt-1 font-medium">Processing</span>
                    </div>
                );
            case DocumentStatus.ERROR:
                 return (
                    <div className="flex flex-col items-center text-red-500">
                        <XCircleIcon className="w-6 h-6" />
                        <span className="text-xs mt-1 font-medium">Failed</span>
                    </div>
                );
            case DocumentStatus.DUPLICATE:
                return (
                    <div className="flex flex-col items-center text-yellow-500">
                        <DocumentDuplicateIcon className="w-6 h-6" />
                        <span className="text-xs mt-1 font-medium">{document.status}</span>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="flex justify-center items-center h-full">
            {getStatusIndicator()}
        </div>
    );
};

export default DocumentStatusCell;
