import type React from "react";

import { useState, useEffect } from "react";
import { Send, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Markdown } from "@/components/markdown";
import { useTheme } from "@/hooks/use-theme";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface LegalResult {
  book_roman: string;
  book_name: string;
  chapter_roman: string;
  chapter_name: string;
  title_roman: string;
  title_name: string;
  section_roman_or_arabic: string;
  section_name: string;
  article_number: string;
  article_name: string;
  content: string;
}
interface ApiResponse {
  results: LegalResult[];
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // Ensure theme component doesn't render until mounted on client
  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Make API request
      const response = await fetch(
        "http://127.0.0.1:8000/api/chat/completions?api_key=c21842a475ac4a2c52d102b7f3a1da4d",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: input,
            top_k: 3,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch response");
      }

      const data: ApiResponse = await response.json();

      // Format the results as markdown
      const markdownContent = formatResultsAsMarkdown(data.results);

      // Add assistant message
      const assistantMessage: Message = {
        role: "assistant",
        content: markdownContent,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, there was an error processing your request.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatResultsAsMarkdown = (results: LegalResult[]): string => {
    return results
      .map(
        (result) => `## Article ${result.article_number}: ${result.article_name}
**Book ${result.book_roman}: ${result.book_name} > Chapter ${
          result.chapter_roman
        }: ${result.chapter_name}${
          result.section_name
            ? ` > Section ${result.section_roman_or_arabic}: ${result.section_name}`
            : ""
        }**

${result.content}
`
      )
      .join("\n\n---\n\n");
  };

  if (!mounted) {
    // Return a placeholder with the same dimensions to prevent layout shift
    return (
      <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Legal Assistant</h1>
          <div className="w-9 h-9"></div>
        </div>
        <div className="flex-1"></div>
        <div className="h-10"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen md:px-20 mx-auto p-4 dark:bg-gray-900 dark:text-white">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Legal Assistant</h1>
      </div>
      <ScrollArea type="always" className="h-full overflow-y-auto my-1">
        <div className="h-full">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 mt-10">
              <p>Ask a legal question to get started</p>
            </div>
          ) : (
            messages.map((message, index) => (
              <Card
                key={index}
                className={`p-4 rounded-none border-y-gray-600 border-x-0 ${
                  message.role === "user"
                    ? "bg-blue-50 dark:bg-blue-900/30"
                    : "bg-white dark:bg-gray-800"
                }`}
              >
                <div className="font-semibold mb-2">
                  {message.role === "user" ? "You" : "Legal Assistant"}
                </div>
                {message.role === "assistant" ? (
                  <Markdown content={message.content} />
                ) : (
                  <p>{message.content}</p>
                )}
              </Card>
            ))
          )}

          {isLoading && (
            <Card className="p-4 bg-white dark:bg-gray-800 rounded-none">
              <div className="font-semibold mb-2">Legal Assistant</div>
              <div className="flex items-center space-x-2">
                <div className="animate-pulse h-2 w-2 bg-gray-400 rounded-full"></div>
                <div className="animate-pulse h-2 w-2 bg-gray-400 rounded-full"></div>
                <div className="animate-pulse h-2 w-2 bg-gray-400 rounded-full"></div>
              </div>
            </Card>
          )}
        </div>
        <ScrollBar orientation="vertical" className="h-full" />
      </ScrollArea>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your legal question..."
          disabled={isLoading}
          className="flex-1 dark:bg-gray-800 dark:border-gray-700"
        />
        <Button
          type="submit"
          disabled={isLoading}
          className="dark:bg-gray-800 dark:border-gray-700"
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
}
