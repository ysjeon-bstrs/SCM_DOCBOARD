
import { GoogleGenAI, Type } from '@google/genai';
import { AnalyzedData, DocumentType } from '../types';

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  console.warn("API_KEY environment variable not set. Using a mock service.");
}

const ai = API_KEY ? new GoogleGenAI({ apiKey: API_KEY }) : null;

const MOCK_DELAY = 1500;

const mockGeminiService = (
  fileContent: string,
  docType: DocumentType
): Promise<Omit<AnalyzedData, 'shipmentId'>> => {
  console.log(`--- MOCK AI ANALYSIS FOR: ${docType} ---`);
  console.log(fileContent.substring(0, 100) + '...');
  return new Promise(resolve => {
    setTimeout(() => {
      const randomSku = () => `SKU${Math.floor(1000 + Math.random() * 9000)}`;
      const totalAmount = parseFloat((Math.random() * 10000 + 500).toFixed(2));
      const quantity = Math.floor(Math.random() * 200 + 10);
      const result = {
        invoiceNumber: `INV-${Date.now().toString().slice(-6)}`,
        totalAmount,
        quantity,
        skus: [randomSku(), randomSku(), randomSku()],
        analysisSummary: `This document appears to be a ${docType} for a shipment of ${quantity} items, with a total value of $${totalAmount}.`,
      };
      console.log('--- MOCK AI RESPONSE ---', result);
      resolve(result);
    }, MOCK_DELAY);
  });
};


export const analyzeDocumentContent = async (
    fileContent: string,
    docType: DocumentType
): Promise<Omit<AnalyzedData, 'shipmentId'>> => {

    if (!ai) {
        return mockGeminiService(fileContent, docType);
    }
    
    const prompt = `Analyze the following document content, which is a "${docType}". Extract the following information:
    1. The invoice number.
    2. The total monetary amount (as a number).
    3. The total quantity of all items.
    4. A list of all unique SKU codes.
    5. A brief, one-sentence summary of the document's key content.
    
    Document Content:
    "${fileContent}"
    
    Return the data in the specified JSON format.`;

    try {
        const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: prompt,
            config: {
                responseMimeType: "application/json",
                responseSchema: {
                    type: Type.OBJECT,
                    properties: {
                        invoiceNumber: { type: Type.STRING, description: "The invoice or shipment identification number." },
                        totalAmount: { type: Type.NUMBER, description: "The total monetary value of the shipment." },
                        quantity: { type: Type.INTEGER, description: "The total number of individual items." },
                        skus: { 
                            type: Type.ARRAY,
                            items: { type: Type.STRING },
                            description: "A list of unique Stock Keeping Units (SKUs)."
                        },
                        analysisSummary: { type: Type.STRING, description: "A brief one-sentence summary of the document's key content." }
                    },
                    required: ["invoiceNumber", "totalAmount", "quantity", "skus", "analysisSummary"]
                },
            },
        });
        
        const jsonString = response.text;
        const result = JSON.parse(jsonString);

        return {
            invoiceNumber: result.invoiceNumber,
            totalAmount: result.totalAmount,
            quantity: result.quantity,
            skus: result.skus,
            analysisSummary: result.analysisSummary
        };

    } catch (error) {
        console.error("Error calling Gemini API:", error);
        throw new Error("Failed to parse document with Gemini API.");
    }
};
