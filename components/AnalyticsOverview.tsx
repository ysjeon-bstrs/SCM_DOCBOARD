
import React from 'react';

interface AnalyticsOverviewProps {
  summary: {
    totalDocs: number;
    uploadedDocs: number;
    missingDocs: number;
    totalValue: number;
  };
}

const StatCard: React.FC<{ title: string; value: string | number; description: string; children: React.ReactNode }> = ({ title, value, description, children }) => (
  <div className="bg-white p-6 rounded-lg shadow">
    <div className="flex items-center">
      <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
        {children}
      </div>
      <div className="ml-5 w-0 flex-1">
        <dl>
          <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
          <dd className="flex items-baseline">
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
          </dd>
        </dl>
      </div>
    </div>
  </div>
);

const AnalyticsOverview: React.FC<AnalyticsOverviewProps> = ({ summary }) => {
  const { totalDocs, uploadedDocs, missingDocs, totalValue } = summary;
  const completionPercentage = totalDocs > 0 ? ((uploadedDocs / totalDocs) * 100).toFixed(1) : 0;

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Dashboard Overview</h2>
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Shipment Value" value={`$${new Intl.NumberFormat().format(totalValue)}`} description="From analyzed documents">
            <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v.01" /></svg>
        </StatCard>
        <StatCard title="Documents Uploaded" value={uploadedDocs} description="All time">
             <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </StatCard>
        <StatCard title="Documents Missing" value={missingDocs} description="Needs attention">
            <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
        </StatCard>
         <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Completion Rate</h3>
            <div className="mt-4 flex items-baseline space-x-2">
                 <p className="text-2xl font-semibold text-gray-900">{completionPercentage}%</p>
                 <p className="text-sm text-gray-500">of {totalDocs} total docs</p>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                <div className="bg-indigo-600 h-2.5 rounded-full" style={{ width: `${completionPercentage}%` }}></div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsOverview;
