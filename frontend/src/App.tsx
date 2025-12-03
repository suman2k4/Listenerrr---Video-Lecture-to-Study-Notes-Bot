import { useState } from 'react';
import UploadForm from './components/UploadForm';
import StatusCard from './components/StatusCard';

export default function App() {
  const [jobId, setJobId] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white shadow">
        <div className="mx-auto max-w-5xl px-4 py-6">
          <h1 className="text-2xl font-semibold text-slate-900">Listenerrr</h1>
          <p className="text-sm text-slate-500">Lecture → Study Notes automation</p>
        </div>
      </header>
      <main className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-8">
        <UploadForm onJobCreated={setJobId} />
        {jobId && <StatusCard jobId={jobId} />}
      </main>
    </div>
  );
}
