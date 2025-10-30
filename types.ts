
export enum DocumentType {
    INVOICE = 'Commercial Invoice',
    BILL_OF_LADING = 'Bill of Lading (BL)',
    PACKING_LIST = 'Packing List',
    CERTIFICATE_OF_ORIGIN = 'Certificate of Origin',
    CUSTOMS_DECLARATION = 'Customs Declaration',
    SETTLEMENT_STATEMENT = 'Settlement Statement',
}

export enum DocumentStatus {
    MISSING = 'Missing',
    UPLOADED = 'Uploaded',
    PROCESSING = 'Processing',
    DUPLICATE = 'Duplicate',
    ERROR = 'Error'
}

export interface Document {
    name: string;
    status: DocumentStatus;
    uploadDate?: string;
    uploader?: string;
    driveLink?: string;
    analysisSummary?: string;
}

export interface Shipment {
    id: string;
    invoiceNumber: string;
    shippingDate: string;
    origin: string;
    destination: string;
    carrier: string;
    documents: {
        [key in DocumentType]: Pick<Document, 'status'> & Partial<Omit<Document, 'status'>>;
    };
}

export interface AnalyzedData {
    shipmentId: string;
    invoiceNumber?: string;
    totalAmount?: number;
    quantity?: number;
    skus?: string[];
    analysisSummary?: string;
}

export interface UploadLogEntry {
    id: string;
    fileName: string;
    driveLink: string;
    uploadTimestamp: string;
    documentType: DocumentType;
    uploader: string;
    shipmentId: string;
    analysisStatus: 'Success' | 'Failed';
    comments?: string;
    extractedData?: Omit<AnalyzedData, 'shipmentId'>;
}

export interface ModalState {
    isOpen: boolean;
    shipmentId?: string;
    docType?: DocumentType;
    file?: File;
}
