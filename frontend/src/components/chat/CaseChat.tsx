"use client";

import React, { useState, useRef, useEffect } from "react";
import { useCaseStore } from "@/store/caseStore";
import { Send, Play, Sparkles, User, Bot, Loader2, CheckCircle2, UserCheck, MapPin, Scale } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export function CaseChat() {
  const {
    sessionId,
    language,
    messages,
    isInvestigating,
    extractedFacts,
    suggestedOptions,
    isReadyToLaunch,
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
    setExtractedFacts,
    setSuggestedOptions,
    setIsReadyToLaunch,
  } = useCaseStore();

  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat internally to bottom without moving window
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTo({
        top: messagesContainerRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
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
      if (data.options) {
        setSuggestedOptions(data.options);
      }
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

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputMessage).trim();
    if (!text) return;

    setInputMessage("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "42px";
    }
    addMessage({ role: "user", content: text });

    let activeSessionId = sessionId;
    if (!activeSessionId) {
      activeSessionId = "case-" + Math.random().toString(36).substring(7);
      setSessionId(activeSessionId);
    }

    setIsTyping(true);
    updateAgentStatus("intake_agent", "thinking", "Analyzing response and updating case memory...");

    try {
      const res = await fetch(`${API_BASE}/case/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: activeSessionId, message: text }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.reply) {
          addMessage({ role: "assistant", content: data.reply });
        }
        if (data.extracted_facts) {
          setExtractedFacts(data.extracted_facts);
        }
        if (data.options) {
          setSuggestedOptions(data.options);
        }
        if (data.ready_to_launch !== undefined) {
          setIsReadyToLaunch(data.ready_to_launch);
        }
        updateAgentStatus("intake_agent", "completed", "Facts updated in memory.");
      }
    } catch (err) {
      console.warn("Message response fallback", err);
      updateAgentStatus("intake_agent", "completed", "Fact discovery active.");
    } finally {
      setIsTyping(false);
    }
  };

  // Option Chip Click Handler
  const handleOptionClick = (opt: string) => {
    if (opt.startsWith("🚀") || opt.includes("Investigation")) {
      handleTriggerInvestigation();
    } else {
      handleSendMessage(opt);
    }
  };

  // Handle Enter key for submission (Shift+Enter for newline)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Launch Full 8-Agent Investigation with Dynamic Case Facts
  const handleTriggerInvestigation = async () => {
    if (!sessionId) return;
    setIsInvestigating(true);

    // Build heirs list from extracted facts or defaults
    const sonsCount = extractedFacts.sons_count ?? 0;
    const daughtersCount = extractedFacts.daughters_count ?? 0;
    const widowAlive = extractedFacts.widow_alive ?? false;
    const wivesCount = extractedFacts.wives_count ?? (widowAlive ? 1 : 0);
    const motherAlive = extractedFacts.mother_alive ?? false;
    const fatherAlive = extractedFacts.father_alive ?? false;
    const deceasedName = extractedFacts.deceased_name || "Late Deceased";
    const dateOfDeath = extractedFacts.date_of_death || "2023-01-14";
    const propertyArea = extractedFacts.property_area || "Family Estate";
    const propertyLocation = extractedFacts.location || "Pakistan";
    const disputeReason = extractedFacts.dispute_type || "Brothers unlawfully dispossessing claimant sisters of inheritance";

    const familyMembers = [];
    if (widowAlive || wivesCount > 0) {
      for (let w = 0; w < Math.max(1, wivesCount); w++) {
        familyMembers.push({
          name: wivesCount === 1 ? "Widow" : `Widow #${w + 1}`,
          relationship_to_deceased: "wife",
          is_alive: true,
          gender: "female",
          is_claimant: false,
        });
      }
    }
    if (motherAlive) {
      familyMembers.push({
        name: "Mother",
        relationship_to_deceased: "mother",
        is_alive: true,
        gender: "female",
        is_claimant: false,
      });
    }
    if (fatherAlive) {
      familyMembers.push({
        name: "Father",
        relationship_to_deceased: "father",
        is_alive: true,
        gender: "male",
        is_claimant: false,
      });
    }
    for (let s = 0; s < sonsCount; s++) {
      familyMembers.push({
        name: sonsCount > 1 ? `Brother #${s + 1}` : "Brother",
        relationship_to_deceased: "son",
        is_alive: true,
        gender: "male",
        is_claimant: false,
      });
    }
    for (let d = 0; d < daughtersCount; d++) {
      const isClaimant = d === 0;
      familyMembers.push({
        name: isClaimant ? "Claimant (Daughter)" : `Sister #${d}`,
        relationship_to_deceased: "daughter",
        is_alive: true,
        gender: "female",
        is_claimant: isClaimant,
      });
    }

    const dynamicIntake = {
      case_id: sessionId,
      claimant_name: "Claimant Daughter",
      claimant_language: language,
      deceased_name: deceasedName,
      date_of_death: dateOfDeath,
      sect: "Hanafi",
      family_members: familyMembers,
      properties: [
        {
          location: propertyLocation,
          area_description: propertyArea,
          estimated_value_pkr: 0.0,
          claimed_documents: ["Deed / Mutation Record", disputeReason],
        },
      ],
      alleged_fraud_description: disputeReason,
    };

    try {
      await fetch(`${API_BASE}/case/investigate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          intake_data: dynamicIntake,
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

  const hasAnyFacts = Object.keys(extractedFacts).length > 0;

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
            <p className="text-[11px] text-slate-500">Autonomous Conversational Discovery</p>
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

      {/* Live Discovered Case Facts Badge Bar */}
      {hasAnyFacts && (
        <div className="px-4 py-2 bg-primary-50/80 border-b border-primary-100 flex flex-wrap items-center gap-2 text-[11px]">
          <span className="font-bold text-primary-900 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>Case Facts Locked:</span>
          </span>
          {extractedFacts.deceased_name && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              <UserCheck className="w-3 h-3 text-primary-600" />
              {extractedFacts.deceased_name}
              {extractedFacts.date_of_death && <span className="text-[10px] text-slate-500 font-normal">({extractedFacts.date_of_death})</span>}
            </span>
          )}
          {(extractedFacts.sons_count !== undefined || extractedFacts.daughters_count !== undefined) && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              👨‍👩‍👧‍👦 {extractedFacts.sons_count || 0} Sons, {extractedFacts.daughters_count || 0} Daughters
            </span>
          )}
          {extractedFacts.widow_alive && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              💍 {extractedFacts.wives_count ? `${extractedFacts.wives_count} Widow(s)` : "Widow"}
            </span>
          )}
          {extractedFacts.mother_alive && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              👵 Mother
            </span>
          )}
          {extractedFacts.father_alive && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              👴 Father
            </span>
          )}
          {extractedFacts.property_area && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              <Scale className="w-3 h-3 text-accent-600" />
              {extractedFacts.property_area}
            </span>
          )}
          {extractedFacts.location && (
            <span className="bg-white px-2 py-0.5 rounded-md border border-primary-200 text-primary-800 font-semibold flex items-center gap-1">
              <MapPin className="w-3 h-3 text-red-500" />
              {extractedFacts.location}
            </span>
          )}
        </div>
      )}

      {/* Quick Benchmark Preset */}
      <div className="px-4 py-2 bg-accent-50/50 border-b border-accent-100 flex items-center justify-between text-xs">
        <div className="flex items-center gap-1.5 text-accent-700 font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-accent-600" />
          <span>Quick Demo Scenario:</span>
        </div>
        <button
          onClick={handleLoadFatimaCase}
          className="px-2.5 py-1 bg-accent-600 hover:bg-accent-700 text-white font-bold rounded-lg text-[11px] transition-colors shadow-xs"
        >
          Load Fatima&apos;s Case (120 Kanals)
        </button>
      </div>

      {/* Message Stream */}
      <div ref={messagesContainerRef} className="flex-1 p-4 overflow-y-auto space-y-3">
        {messages.length === 0 && (
          <div className="text-center py-10">
            <div className="w-12 h-12 rounded-2xl bg-primary-50 text-primary-800 flex items-center justify-center mx-auto mb-3 font-bold text-lg">
              ⚖️
            </div>
            <h3 className="font-bold text-slate-800 text-sm mb-1">Start Your Case Discovery</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mb-4">
              Type your grievance in English or Roman Urdu to start the intelligent intake interview.
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
      </div>

      {/* Suggested Quick-Reply Option Chips */}
      {suggestedOptions && suggestedOptions.length > 0 && !isInvestigating && (
        <div className="px-3 pt-2 pb-1 bg-slate-50/70 border-t border-slate-200 flex flex-wrap gap-1.5 items-center">
          <span className="text-[10px] uppercase font-bold text-slate-400 mr-1">Quick Select:</span>
          {suggestedOptions.map((opt, i) => (
            <button
              key={i}
              onClick={() => handleOptionClick(opt)}
              className={`px-2.5 py-1 text-[11px] font-semibold rounded-lg border transition-all ${
                opt.startsWith("🚀")
                  ? "bg-emerald-600 hover:bg-emerald-700 text-white border-emerald-700 shadow-xs animate-bounce"
                  : "bg-white hover:bg-slate-100 text-slate-700 border-slate-300"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}

      {/* Action Bar & Multiline Input */}
      <div className="p-3 border-t border-border bg-white space-y-2">
        {sessionId && !isInvestigating && (
          <button
            onClick={handleTriggerInvestigation}
            className={`w-full py-2.5 text-white text-xs font-bold rounded-xl flex items-center justify-center gap-2 shadow-xs transition-all ${
              isReadyToLaunch
                ? "bg-emerald-600 hover:bg-emerald-700 ring-2 ring-emerald-400/40"
                : "bg-success-600 hover:bg-success-700"
            }`}
          >
            <Play className="w-4 h-4 fill-white" />
            {isReadyToLaunch ? "All Facts Complete — Launch 8-Agent Investigation" : "Launch 8-Agent Autonomous Investigation"}
          </button>
        )}

        {isInvestigating && (
          <div className="w-full py-2 bg-info-50 text-info-700 border border-info-200 text-xs font-semibold rounded-xl flex items-center justify-center gap-2 animate-pulse">
            <Loader2 className="w-4 h-4 animate-spin text-info-600" />
            Autonomous Agents Investigating in Real Time...
          </div>
        )}

        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex items-end gap-2">
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
