
import React from 'react';
import { Shipment } from '../types';
import ShipmentRow from './ShipmentRow';
import { DOCUMENT_TYPES } from '../constants';

interface DashboardProps {
    shipments: Shipment[];
}

const Dashboard: React.FC<DashboardProps> = ({ shipments }) => {
    return (
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold leading-6 text-gray-900">Shipment Document Status</h2>
                <p className="mt-1 text-sm text-gray-500">Overview of all ongoing shipments and their required documentation.</p>
            </div>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice #</th>
                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                            {DOCUMENT_TYPES.map(docType => (
                                <th key={docType} scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">{docType.split('(')[0].trim()}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {shipments.map(shipment => (
                            <ShipmentRow key={shipment.id} shipment={shipment} />
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Dashboard;
