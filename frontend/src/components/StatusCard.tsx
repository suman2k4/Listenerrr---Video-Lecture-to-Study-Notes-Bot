import { useEffect, useState } from 'react';
import axios from 'axios';

declare const __API_BASE__: string;

interface Props {
  jobId: string;
}

interface JobMeta {
  progress?: Array<{ stage: string; message: string; ts: number }>;
  artifacts?: Record<string, string>;
}

export default function StatusCard({ jobId }: Props) {
  const [status, setStatus] = useState('queued');
  const [stage, setStage] = useState('uploading');
  const [meta, setMeta] = useState<JobMeta>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let timer: number;
    const fetchStatus = async () => {
      try {
        const { data } = await axios.get(`${__API_BASE__}/jobs/${jobId}`);
        setStatus(data.status);
        setStage(data.stage);
        setMeta(data.meta);
        setError(null);
        if (!['finished', 'failed'].includes(data.status)) {
          timer = window.setTimeout(fetchStatus, 2000);
        }
      } catch (err) {
        setError('Failed to load status');
        console.error(err);
      }
    };
    fetchStatus();
    return () => window.clearTimeout(timer);
  }, [jobId]);

  return (
    <section className="rounded-lg bg-white p-6 shadow">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Job Status</h2>
          <p className="text-sm text-slate-500">Tracking ID: {jobId}</p>
        </div>
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
          {status} / {stage}
        </span>
      </div>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      <ul className="mt-4 space-y-2 text-sm text-slate-600">
        {(meta.progress ?? []).slice(-5).map((entry) => (
          <li key={`${entry.stage}-${entry.ts}`} className="rounded border border-slate-200 px-3 py-2">
            <strong className="font-semibold text-slate-800">{entry.stage}</strong>
            <span className="ml-2">{entry.message}</span>
          </li>
        ))}
        {(!meta.progress || meta.progress.length === 0) && <li>No progress recorded yet.</li>}
      </ul>
    </section>
  );
}
