
import React from 'react';
import { UploadLogEntry, Shipment } from '../types';
import { CheckCircleIcon } from './icons/CheckCircleIcon';
import { XCircleIcon } from './icons/XCircleIcon';

interface UploadLogsProps {
    logs: UploadLogEntry[];
    shipments: Shipment[];
}

const UploadLogs: React.FC<UploadLogsProps> = ({ logs, shipments }) => {
    const getInvoiceNumber = (shipmentId: string) => {
        return shipments.find(s => s.id === shipmentId)?.invoiceNumber || shipmentId;
    }

    return (
        <div className="bg-white shadow-md rounded-lg h-full">
            <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold leading-6 text-gray-900">Recent Activity</h2>
                <p className="mt-1 text-sm text-gray-500">Log of all document uploads and analyses.</p>
            </div>
            <div className="overflow-y-auto max-h-[calc(100vh-250px)]">
                {logs.length === 0 ? (
                    <div className="text-center py-12 px-6">
                        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                        </svg>
                        <h3 className="mt-2 text-sm font-medium text-gray-900">No recent activity</h3>
                        <p className="mt-1 text-sm text-gray-500">Upload a document to get started.</p>
                    </div>
                ) : (
                <ul role="list" className="divide-y divide-gray-200">
                    {logs.map((log) => (
                        <li key={log.id} className="p-4 hover:bg-gray-50">
                            <div className="flex items-center space-x-4">
                                <div className="flex-shrink-0">
                                    {log.analysisStatus === 'Success' ? (
                                        <CheckCircleIcon className="h-8 w-8 text-green-500" />
                                    ) : (
                                        <XCircleIcon className="h-8 w-8 text-red-500" />
                                    )}
                                </div>
                                <div className="min-w-0 flex-1">
                                    <p className="truncate text-sm font-medium text-gray-900" title={log.fileName}>{log.fileName}</p>
                                    <p className="truncate text-sm text-gray-500">
                                        <span className="font-semibold">{getInvoiceNumber(log.shipmentId)}</span> - <span>{log.documentType}</span>
                                    </p>
                                    <p className="text-xs text-gray-400 mt-1">
                                        {new Date(log.uploadTimestamp).toLocaleString()} by {log.uploader}
                                    </p>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
                )}
            </div>
        </div>
    );
};

export default UploadLogs;
