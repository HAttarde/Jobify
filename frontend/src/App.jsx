import React, { useState } from 'react';

function App() {
    const [resume, setResume] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [role, setRole] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResults(null);

        try {
            const response = await fetch('http://localhost:5001/api/process-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ resume, job_description: jobDescription, company_name: companyName, role }),
            });

            if (!response.ok) {
                throw new Error('Something went wrong on the server.');
            }

            const data = await response.json();
            console.log('Received data:', data); // Debug log
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 font-sans text-gray-800">
            <div className="container mx-auto p-8">
                <header className="text-center mb-12">
                    <h1 className="text-5xl font-bold text-gray-900">AI Job Application Agent</h1>
                    <p className="text-xl text-gray-600 mt-2">Your personal assistant for landing your dream job.</p>
                </header>

                <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                            <div>
                                <label htmlFor="companyName" className="block text-lg font-semibold mb-2">Company Name</label>
                                <input type="text" id="companyName" value={companyName} onChange={(e) => setCompanyName(e.target.value)} className="w-full p-3 border rounded-md" placeholder="e.g., Google" required />
                            </div>
                            <div>
                                <label htmlFor="role" className="block text-lg font-semibold mb-2">Role</label>
                                <input type="text" id="role" value={role} onChange={(e) => setRole(e.target.value)} className="w-full p-3 border rounded-md" placeholder="e.g., Software Engineer" required />
                            </div>
                        </div>
                        <div className="mb-6">
                            <label htmlFor="resume" className="block text-lg font-semibold mb-2">Your Base Resume</label>
                            <textarea id="resume" value={resume} onChange={(e) => setResume(e.target.value)} className="w-full p-3 border rounded-md" rows="10" placeholder="Paste your resume here..." required></textarea>
                        </div>
                        <div className="mb-8">
                            <label htmlFor="jobDescription" className="block text-lg font-semibold mb-2">Job Description</label>
                            <textarea id="jobDescription" value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} className="w-full p-3 border rounded-md" rows="10" placeholder="Paste the job description here..." required></textarea>
                        </div>
                        <div className="text-center">
                            <button type="submit" disabled={loading} className="bg-blue-600 text-white font-bold py-3 px-8 rounded-full hover:bg-blue-700 transition duration-300 disabled:bg-gray-400">
                                {loading ? 'Processing...' : 'Generate Application Materials'}
                            </button>
                        </div>
                    </form>
                </div>

                {error && <div className="mt-8 text-center text-red-500 font-semibold">{error}</div>}
                
                {results && (
                    <div className="mt-12">
                        <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto mb-8">
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="text-3xl font-bold">Tailored Resume</h2>
                                <button 
                                    onClick={() => {
                                        const blob = new Blob([results.tailored_resume], { type: 'text/plain' });
                                        const url = URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = 'tailored_resume.txt';
                                        a.click();
                                    }}
                                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
                                >
                                    Download Resume
                                </button>
                            </div>
                            <div className="bg-white border border-gray-300 p-8 rounded-md shadow-sm" style={{ fontFamily: 'Georgia, serif', lineHeight: '1.6' }}>
                                <pre className="whitespace-pre-wrap text-sm" style={{ fontFamily: 'Georgia, serif' }}>
                                    {results.tailored_resume || "No resume generated."}
                                </pre>
                            </div>
                            
                            <div className="flex justify-between items-center mt-8 mb-4">
                                <h2 className="text-3xl font-bold">Cover Letter</h2>
                                <button 
                                    onClick={() => {
                                        const blob = new Blob([results.cover_letter], { type: 'text/plain' });
                                        const url = URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = 'cover_letter.txt';
                                        a.click();
                                    }}
                                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
                                >
                                    Download Cover Letter
                                </button>
                            </div>
                            <div className="bg-white border border-gray-300 p-8 rounded-md shadow-sm" style={{ fontFamily: 'Georgia, serif', lineHeight: '1.6' }}>
                                <pre className="whitespace-pre-wrap text-sm" style={{ fontFamily: 'Georgia, serif' }}>
                                    {results.cover_letter || "No cover letter generated."}
                                </pre>
                            </div>
                        </div>
                        
                        {results.outreach && results.outreach.length > 0 && (
                            <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-3xl font-bold">Outreach Materials</h2>
                                    <button 
                                        onClick={() => {
                                            const outreachText = results.outreach.map((contact, i) => 
                                                `Contact ${i + 1}: ${contact.name}\n` +
                                                `Title: ${contact.title}\n` +
                                                `LinkedIn: ${contact.linkedin}\n` +
                                                `Email: ${contact.email}\n\n` +
                                                `LinkedIn Note:\n${contact.linkedin_note}\n\n` +
                                                `Cold Email:\n${contact.cold_email}\n\n` +
                                                `${'='.repeat(80)}\n\n`
                                            ).join('');
                                            
                                            const blob = new Blob([outreachText], { type: 'text/plain' });
                                            const url = URL.createObjectURL(blob);
                                            const a = document.createElement('a');
                                            a.href = url;
                                            a.download = 'outreach_contacts.txt';
                                            a.click();
                                        }}
                                        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
                                    >
                                        Download All Contacts
                                    </button>
                                </div>
                                {results.outreach.map((contact, index) => (
                                    <div key={index} className="mb-8 pb-8 border-b last:border-b-0">
                                        <h3 className="text-2xl font-semibold mb-2">
                                            {contact.name} - <span className="text-lg text-gray-600">{contact.title}</span>
                                        </h3>
                                        <div className="mb-4 space-y-1">
                                            <p className="text-blue-600">
                                                <a href={contact.linkedin} target="_blank" rel="noopener noreferrer" className="hover:underline">
                                                    {contact.linkedin}
                                                </a>
                                            </p>
                                            <p className="text-gray-700">{contact.email}</p>
                                        </div>
                                        
                                        <div className="mt-4">
                                            <h4 className="font-bold text-lg mb-2">LinkedIn Connection Note:</h4>
                                            <p className="bg-blue-50 p-3 rounded-md italic text-sm border-l-4 border-blue-500">
                                                "{contact.linkedin_note}"
                                            </p>
                                        </div>
                                        
                                        <div className="mt-4">
                                            <h4 className="font-bold text-lg mb-2">Cold Email:</h4>
                                            <pre className="whitespace-pre-wrap bg-gray-50 p-3 rounded-md text-sm">
                                                {contact.cold_email}
                                            </pre>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;