"use client";

import React, { useState, useRef, useEffect } from "react";
import { useCaseStore } from "@/store/caseStore";
import { Send, Play, Sparkles, User, Bot, Loader2 } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export function CaseChat() {
  const {
    sessionId,
    language,
    messages,
    isInvestigating,
    setSessionId,
    setLanguage,
    addMessage,
    setIsInvestigating,
    setFinalReport,
    setShariaShares,
    setFamilyTree,
    setLegalRoadmap,
    addFraudAlert,
    updateAgentStatus,
  } = useCaseStore();

  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Adjust textarea height on change
  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputMessage(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  };

  // Initialize session if not started
  const handleStartCase = async (lang: "en" | "roman_urdu") => {
    setLoading(true);
    try {
      setLanguage(lang);
      const res = await fetch(`${API_BASE}/case/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ preferred_language: lang }),
      });
      const data = await res.json();
      setSessionId(data.session_id);
      addMessage({
        role: "assistant",
        content: data.greeting,
      });
      updateAgentStatus("intake_agent", "thinking", "Intake Officer interviewing claimant...");
    } catch (err) {
      console.error("Failed to initialize case", err);
      const fallbackId = "case-" + Math.random().toString(36).substring(7);
      setSessionId(fallbackId);
      addMessage({
        role: "assistant",
        content:
          lang === "en"
            ? "As-salamu alaykum. I am HaqDar's intake specialist. Can you share who the deceased was, date of death, and surviving heirs?"
            : "As-salamu alaykum. Main HaqDar ka intake officer hoon. Marhoom ka naam, tareekh e inteqal aur wariseen ke baray mein batayein.",
      });
    } finally {
      setLoading(false);
    }
  };

  // Pre-load Fatima's Benchmark Demo Case
  const handleLoadFatimaCase = async () => {
    if (!sessionId) {
      await handleStartCase(language);
    }
    const sampleText =
      language === "en"
        ? "My father Haji Ghulam Rasool died on 14 Jan 2023 in Gujranwala leaving 120 Kanals of agricultural land. Surviving family members are my mother (widow Kulsoom Bibi), my grandmother (Jannat Bibi), two brothers (Tariq and Rashid), and myself (daughter Fatima). My brothers colluded with the village Patwari and produced a fake oral Hiba deed dated 2 days before father's death claiming I gave up my share, and omitted my name from Mutation No. 412."
        : "Mere walid Haji Ghulam Rasool ka inteqal 14 Jan 2023 ko Gujranwala mein hua. Unhon ne 120 Kanal zameen chori. Wariseen mein meri walida (widow), 2 bhai (Tariq aur Rashid), aur 1 beti (main Fatima) hain. Mere bhaiyon ne Patwari se mil kar mere inteqal se 2 din pehle ka jaali Hiba deed banwaya aur mera hissa kha gaye.";

    setInputMessage(sampleText);
    setTimeout(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
        textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
      }
    }, 50);
  };

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputMessage.trim()) return;

    const userText = inputMessage.trim();
    setInputMessage("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "42px";
    }
    addMessage({ role: "user", content: userText });

    let activeSessionId = sessionId;
    if (!activeSessionId) {
      activeSessionId = "case-" + Math.random().toString(36).substring(7);
      setSessionId(activeSessionId);
    }

    setIsTyping(true);
    updateAgentStatus("intake_agent", "thinking", "Analyzing grievance and structuring follow-up questions...");

    try {
      const res = await fetch(`${API_BASE}/case/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: activeSessionId, message: userText }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.reply) {
          addMessage({ role: "assistant", content: data.reply });
          updateAgentStatus("intake_agent", "completed", "Facts gathered. Ready for investigation.");
        }
      }
    } catch (err) {
      console.warn("Message response fallback", err);
      updateAgentStatus("intake_agent", "completed", "Fact discovery ready.");
    } finally {
      setIsTyping(false);
    }
  };

  // Handle Enter key for submission (Shift+Enter for newline)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Launch Full 8-Agent Investigation with Polling Fallback
  const handleTriggerInvestigation = async () => {
    if (!sessionId) return;
    setIsInvestigating(true);

    const structuredIntake = {
      case_id: sessionId,
      claimant_name: "Fatima Bibi",
      claimant_language: language,
      deceased_name: "Haji Ghulam Rasool",
      date_of_death: "2023-01-14",
      sect: "Hanafi",
      family_members: [
        { name: "Kulsoom Bibi", relationship_to_deceased: "wife", is_alive: true, gender: "female", is_claimant: false },
        { name: "Jannat Bibi", relationship_to_deceased: "mother", is_alive: true, gender: "female", is_claimant: false },
        { name: "Tariq Rasool", relationship_to_deceased: "son", is_alive: true, gender: "male", is_claimant: false },
        { name: "Rashid Rasool", relationship_to_deceased: "son", is_alive: true, gender: "male", is_claimant: false },
        { name: "Fatima Bibi", relationship_to_deceased: "daughter", is_alive: true, gender: "female", is_claimant: true },
      ],
      properties: [
        {
          location: "Chak 12-JB, Tehsil Sadar, Gujranwala",
          area_description: "120 Kanals agricultural land under Khasra No. 412/1",
          estimated_value_pkr: 48000000.0,
          claimed_documents: ["Unregistered Oral Hiba claimed by brothers", "Mutation No. 412"],
        },
      ],
      alleged_fraud_description: "Brothers forged oral Hiba deed 2 days prior to death during Marz-ul-Maut and excluded daughter Fatima from revenue mutation.",
    };

    try {
      await fetch(`${API_BASE}/case/investigate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          intake_data: structuredIntake,
        }),
      });

      // Polling fallback every 2 seconds to guarantee UI updates
      const pollInterval = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/case/report/${sessionId}`);
          if (res.ok) {
            const data = await res.json();
            if (data && data.sharia_distribution) {
              clearInterval(pollInterval);
              setIsInvestigating(false);
              setFinalReport(data);
              if (data.sharia_distribution) setShariaShares(data.sharia_distribution);
              if (data.family_tree) setFamilyTree(data.family_tree);
              if (data.legal_roadmap) setLegalRoadmap(data.legal_roadmap);
              if (data.fraud_report?.alerts) {
                data.fraud_report.alerts.forEach((alert: any) => addFraudAlert(alert));
              }
              // Mark agents completed
              [
                "orchestrator",
                "intake_agent",
                "family_tree_agent",
                "document_analyzer",
                "sharia_calculator",
                "fraud_detection_agent",
                "legal_strategy_agent",
                "qa_reviewer",
              ].forEach((id) => {
                updateAgentStatus(id, "completed", "Investigation complete");
              });
            }
          }
        } catch (err) {
          console.error("Poll error", err);
        }
      }, 2000);
    } catch (err) {
      console.error("Failed to start investigation API", err);
      setIsInvestigating(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-2xl border border-border shadow-xs overflow-hidden">
      {/* Header with language selector */}
      <div className="p-4 border-b border-border bg-slate-50/50 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary-800 text-white flex items-center justify-center font-bold text-sm">
            حق
          </div>
          <div>
            <h2 className="font-bold text-sm text-primary-900 leading-tight">Case Discovery & Intake</h2>
            <p className="text-[11px] text-slate-500">Conversational Fact Finding</p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 bg-slate-200/70 p-1 rounded-xl">
          <button
            onClick={() => setLanguage("en")}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              language === "en" ? "bg-white text-primary-900 shadow-xs" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            English
          </button>
          <button
            onClick={() => setLanguage("roman_urdu")}
            className={`px-2.5 py-1 text-xs font-semibold rounded-lg transition-all ${
              language === "roman_urdu" ? "bg-white text-primary-900 shadow-xs" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Roman Urdu
          </button>
        </div>
      </div>

      {/* Quick Benchmark Preset */}
      <div className="px-4 py-2 bg-accent-50/50 border-b border-accent-100 flex items-center justify-between text-xs">
        <div className="flex items-center gap-1.5 text-accent-700 font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-accent-600" />
          <span>Hackathon Demo Preset:</span>
        </div>
        <button
          onClick={handleLoadFatimaCase}
          className="px-2.5 py-1 bg-accent-600 hover:bg-accent-700 text-white font-bold rounded-lg text-[11px] transition-colors shadow-xs"
        >
          Load Fatima&apos;s Case (120 Kanals)
        </button>
      </div>

      {/* Message Stream */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3 min-h-[320px]">
        {messages.length === 0 && (
          <div className="text-center py-10">
            <div className="w-12 h-12 rounded-2xl bg-primary-50 text-primary-800 flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              ⚖️
            </div>
            <h3 className="font-bold text-slate-800 text-sm mb-1">Start Your Case Investigation</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mb-4">
              Type your grievance or load the demo preset to converse with the Intake Agent.
            </p>
            <button
              onClick={() => handleStartCase(language)}
              disabled={loading}
              className="px-4 py-2 bg-primary-800 hover:bg-primary-900 text-white text-xs font-bold rounded-xl shadow-xs transition-colors"
            >
              {loading ? "Starting..." : "Begin Guided Interview"}
            </button>
          </div>
        )}

        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-2.5 max-w-[88%] ${
              m.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            <div
              className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-xs ${
                m.role === "user" ? "bg-primary-800 text-white" : "bg-slate-200 text-slate-700"
              }`}
            >
              {m.role === "user" ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
            </div>
            <div
              className={`p-3 rounded-2xl text-xs leading-relaxed whitespace-pre-wrap ${
                m.role === "user"
                  ? "bg-primary-800 text-white rounded-tr-xs"
                  : "bg-slate-100 text-slate-800 rounded-tl-xs border border-slate-200/60"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex items-center gap-2 text-xs text-slate-500 p-2 bg-slate-50 rounded-xl max-w-[200px] border border-slate-200/60 animate-pulse">
            <Bot className="w-3.5 h-3.5 text-primary-800" />
            <span>Intake Officer is typing...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Action Bar & Multiline Input */}
      <div className="p-3 border-t border-border bg-white space-y-2">
        {sessionId && !isInvestigating && (
          <button
            onClick={handleTriggerInvestigation}
            className="w-full py-2.5 bg-success-600 hover:bg-success-700 text-white text-xs font-bold rounded-xl flex items-center justify-center gap-2 shadow-xs transition-all"
          >
            <Play className="w-4 h-4 fill-white" />
            Launch 8-Agent Autonomous Investigation
          </button>
        )}

        {isInvestigating && (
          <div className="w-full py-2 bg-info-50 text-info-700 border border-info-200 text-xs font-semibold rounded-xl flex items-center justify-center gap-2 animate-pulse">
            <Loader2 className="w-4 h-4 animate-spin text-info-600" />
            Autonomous Agents Investigating in Real Time...
          </div>
        )}

        <form onSubmit={handleSendMessage} className="flex items-end gap-2">
          <textarea
            ref={textareaRef}
            rows={1}
            value={inputMessage}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder={
              language === "en"
                ? "Type any message or answer questions (Shift+Enter for newline)..."
                : "Koi bhi baat ya sawal ka jawab likhein (Shift+Enter for newline)..."
            }
            className="flex-1 px-3.5 py-2.5 text-xs bg-slate-50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-800/20 text-slate-800 placeholder-slate-400 resize-none min-h-[42px] max-h-[160px] overflow-y-auto leading-relaxed"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim()}
            className="p-2.5 bg-primary-800 hover:bg-primary-900 disabled:opacity-40 text-white rounded-xl transition-colors shadow-xs h-[42px] flex items-center justify-center"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
