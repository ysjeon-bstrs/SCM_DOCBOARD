
import React from 'react';
import { Shipment } from '../types';
import DocumentStatusCell from './DocumentStatusCell';
import { DOCUMENT_TYPES } from '../constants';

interface ShipmentRowProps {
    shipment: Shipment;
}

const ShipmentRow: React.FC<ShipmentRowProps> = ({ shipment }) => {
    return (
        <tr className="hover:bg-gray-50 transition-colors duration-150">
            <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">{shipment.invoiceNumber}</div>
                <div className="text-sm text-gray-500">{shipment.id}</div>
            </td>
            <td className="px-3 py-4 whitespace-nowrap text-sm text-gray-500">{shipment.shippingDate}</td>
            <td className="px-3 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900 flex items-center">
                   <span className="font-semibold">{shipment.origin}</span> 
                   <svg className="w-4 h-4 mx-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                   <span className="font-semibold">{shipment.destination}</span>
                </div>
                 <div className="text-xs text-gray-500">{shipment.carrier}</div>
            </td>
            {DOCUMENT_TYPES.map(docType => (
                <td key={docType} className="px-6 py-4 whitespace-nowrap text-center">
                    <DocumentStatusCell 
                        document={shipment.documents[docType]} 
                    />
                </td>
            ))}
        </tr>
    );
};

export default ShipmentRow;
