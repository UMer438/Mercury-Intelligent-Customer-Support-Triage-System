"use client";

import { useState } from "react";
import { AlertCircle, CheckCircle, Clock, Send, Loader2 } from "lucide-react";

interface TicketAnalysis {
  category: string;
  sentiment: string;
  urgency: string;
  suggested_action: string;
  draft_response: string;
}

export default function Home() {
  const [complaint, setComplaint] = useState("");
  const [analysis, setAnalysis] = useState<TicketAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeTicket = async () => {
    if (!complaint.trim()) return;

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ complaint }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze ticket");
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError("Something went wrong. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case "critical":
        return "bg-red-100 text-red-800 border-red-200";
      case "high":
        return "bg-orange-100 text-orange-800 border-orange-200";
      case "medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "low":
        return "bg-green-100 text-green-800 border-green-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900 tracking-tight">
            Mercury
          </h1>
          <p className="text-gray-500 text-lg">
            Intelligent Customer Support System          </p>
        </header>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="complaint"
              className="block text-sm font-medium text-gray-700"
            >
              Customer Complaint
            </label>
            <textarea
              id="complaint"
              rows={4}
              className="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900 p-4 text-base resize-none"
              placeholder="Paste the customer ticket here..."
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
            />
          </div>

          <button
            onClick={analyzeTicket}
            disabled={loading || !complaint.trim()}
            className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Analyze Complaint
              </>
            )}
          </button>

          {error && (
            <div className="p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              {error}
            </div>
          )}
        </div>

        {analysis && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* Category Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-2">
              <div className="flex items-center gap-2 text-gray-500 mb-2">
                <CheckCircle className="w-5 h-5" />
                <span className="text-sm font-medium uppercase tracking-wider">
                  Category
                </span>
              </div>
              <p className="text-xl font-bold text-gray-900">
                {analysis.category.replace(/_/g, " ")}
              </p>
            </div>

            {/* Sentiment Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-2">
              <div className="flex items-center gap-2 text-gray-500 mb-2">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm font-medium uppercase tracking-wider">
                  Sentiment
                </span>
              </div>
              <p className="text-xl font-bold text-gray-900">
                {analysis.sentiment}
              </p>
            </div>

            {/* Urgency Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-2">
              <div className="flex items-center gap-2 text-gray-500 mb-2">
                <Clock className="w-5 h-5" />
                <span className="text-sm font-medium uppercase tracking-wider">
                  Urgency
                </span>
              </div>
              <span
                className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getUrgencyColor(
                  analysis.urgency
                )}`}
              >
                {analysis.urgency}
              </span>
            </div>

            {/* Draft Response - Full Width */}
            <div className="md:col-span-3 bg-white p-6 rounded-2xl shadow-sm border border-gray-100 space-y-4">
              <div className="flex items-center justify-between border-b border-gray-100 pb-4">
                <h3 className="text-lg font-bold text-gray-900">
                  Drafted Response
                </h3>
                <span className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                  Action: {analysis.suggested_action}
                </span>
              </div>
              <div className="prose prose-blue max-w-none">
                <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                  {analysis.draft_response}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
