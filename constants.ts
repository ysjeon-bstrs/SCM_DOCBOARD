
import { Shipment, DocumentStatus, DocumentType } from './types';

export const DOCUMENT_TYPES: DocumentType[] = [
    DocumentType.INVOICE,
    DocumentType.BILL_OF_LADING,
    DocumentType.PACKING_LIST,
    DocumentType.CERTIFICATE_OF_ORIGIN,
    DocumentType.CUSTOMS_DECLARATION,
    DocumentType.SETTLEMENT_STATEMENT,
];

export const INITIAL_SHIPMENTS: Shipment[] = [
    {
        id: 'BSTSE002509010-1',
        invoiceNumber: 'INPHL0002508290044',
        shippingDate: '2025-10-01',
        origin: 'IN',
        destination: 'KR',
        carrier: 'SBSGPH',
        documents: {
            [DocumentType.INVOICE]: { status: DocumentStatus.UPLOADED, name: 'CIPL_BSTSE002509010.pdf', uploadDate: '2024-10-23', uploader: 'Yujin', driveLink: '#' },
            [DocumentType.BILL_OF_LADING]: { status: DocumentStatus.MISSING },
            [DocumentType.PACKING_LIST]: { status: DocumentStatus.MISSING },
            [DocumentType.CERTIFICATE_OF_ORIGIN]: { status: DocumentStatus.UPLOADED, name: 'COO_BSTSE002509010.pdf', uploadDate: '2024-10-24', uploader: 'Admin', driveLink: '#' },
            [DocumentType.CUSTOMS_DECLARATION]: { status: DocumentStatus.MISSING },
            [DocumentType.SETTLEMENT_STATEMENT]: { status: DocumentStatus.MISSING },
        }
    },
    {
        id: 'MV0205020250510-02',
        invoiceNumber: 'INSCG00250830021',
        shippingDate: '2025-10-02',
        origin: 'KR',
        destination: 'US',
        carrier: 'AMZUS',
        documents: {
            [DocumentType.INVOICE]: { status: DocumentStatus.MISSING },
            [DocumentType.BILL_OF_LADING]: { status: DocumentStatus.MISSING },
            [DocumentType.PACKING_LIST]: { status: DocumentStatus.MISSING },
            [DocumentType.CERTIFICATE_OF_ORIGIN]: { status: DocumentStatus.MISSING },
            [DocumentType.CUSTOMS_DECLARATION]: { status: DocumentStatus.MISSING },
            [DocumentType.SETTLEMENT_STATEMENT]: { status: DocumentStatus.MISSING },
        }
    },
    {
        id: 'MV0205020250510-06',
        invoiceNumber: 'MV0205020250510-06',
        shippingDate: '2025-10-08',
        origin: 'KR',
        destination: 'US',
        carrier: 'AMZUS',
        documents: {
            [DocumentType.INVOICE]: { status: DocumentStatus.UPLOADED, name: 'INV_MV0205020250510-06.pdf', uploadDate: '2024-10-23', uploader: 'Yujin', driveLink: '#' },
            [DocumentType.BILL_OF_LADING]: { status: DocumentStatus.UPLOADED, name: 'BL_MV0205020250510-06.pdf', uploadDate: '2024-10-23', uploader: 'Yujin', driveLink: '#' },
            [DocumentType.PACKING_LIST]: { status: DocumentStatus.MISSING },
            [DocumentType.CERTIFICATE_OF_ORIGIN]: { status: DocumentStatus.MISSING },
            [DocumentType.CUSTOMS_DECLARATION]: { status: DocumentStatus.MISSING },
            [DocumentType.SETTLEMENT_STATEMENT]: { status: DocumentStatus.MISSING },
        }
    },
    {
        id: 'MV02110604202510-01',
        invoiceNumber: 'MV02110604202510-01',
        shippingDate: '2025-10-01',
        origin: 'KR',
        destination: 'US',
        carrier: 'CJ대한통운',
        documents: {
            [DocumentType.INVOICE]: { status: DocumentStatus.ERROR },
            [DocumentType.BILL_OF_LADING]: { status: DocumentStatus.MISSING },
            [DocumentType.PACKING_LIST]: { status: DocumentStatus.UPLOADED, name: 'PL_MV02110604202510-01.pdf', uploadDate: '2024-10-22', uploader: 'Jaehyun', driveLink: '#' },
            [DocumentType.CERTIFICATE_OF_ORIGIN]: { status: DocumentStatus.MISSING },
            [DocumentType.CUSTOMS_DECLARATION]: { status: DocumentStatus.MISSING },
            [DocumentType.SETTLEMENT_STATEMENT]: { status: DocumentStatus.MISSING },
        }
    },
    {
        id: 'MV02110604202510-09',
        invoiceNumber: 'MV02110604202510-09',
        shippingDate: '2025-10-01',
        origin: 'KR',
        destination: 'US',
        carrier: 'CJ대한통운',
        documents: {
            [DocumentType.INVOICE]: { status: DocumentStatus.MISSING },
            [DocumentType.BILL_OF_LADING]: { status: DocumentStatus.MISSING },
            [DocumentType.PACKING_LIST]: { status: DocumentStatus.MISSING },
            [DocumentType.CERTIFICATE_OF_ORIGIN]: { status: DocumentStatus.MISSING },
            [DocumentType.CUSTOMS_DECLARATION]: { status: DocumentStatus.MISSING },
            [DocumentType.SETTLEMENT_STATEMENT]: { status: DocumentStatus.MISSING },
        }
    }
];
