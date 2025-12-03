import { FormEvent, useState } from 'react';
import axios from 'axios';

declare const __API_BASE__: string;

interface Props {
  onJobCreated: (jobId: string) => void;
}

export default function UploadForm({ onJobCreated }: Props) {
  const [title, setTitle] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (evt: FormEvent) => {
    evt.preventDefault();
    if (!file && !videoUrl) {
      setError('Provide a URL or upload a file');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const fd = new FormData();
      if (title) fd.append('title', title);
      if (videoUrl) fd.append('video_url', videoUrl);
      if (file) fd.append('file', file);
      const { data } = await axios.post(`${__API_BASE__}/upload`, fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onJobCreated(data.job_id);
    } catch (err) {
      setError('Failed to upload job');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="rounded-lg bg-white p-6 shadow" onSubmit={submit}>
      <h2 className="text-lg font-semibold text-slate-800">Upload Lecture</h2>
      <p className="text-sm text-slate-500">Provide either a video URL or upload a file.</p>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <label className="flex flex-col text-sm text-slate-600">
          Title
          <input className="mt-1 rounded border border-slate-300 px-3 py-2" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Intro to ML" />
        </label>
        <label className="flex flex-col text-sm text-slate-600">
          Video URL
          <input className="mt-1 rounded border border-slate-300 px-3 py-2" value={videoUrl} onChange={(e) => setVideoUrl(e.target.value)} placeholder="https://example.com/lecture.mp4" />
        </label>
      </div>
      <label className="mt-4 flex flex-col text-sm text-slate-600">
        Or upload file
        <input className="mt-1 rounded border border-slate-300 px-3 py-2" type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      </label>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      <button type="submit" disabled={loading} className="mt-4 inline-flex items-center rounded bg-indigo-600 px-4 py-2 text-white disabled:opacity-50">
        {loading ? 'Submitting…' : 'Start Processing'}
      </button>
    </form>
  );
}
