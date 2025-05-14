import ReactMarkdown from "react-markdown";
import { useTheme } from "@/hooks/use-theme";

interface MarkdownProps {
  content: string;
}

export function Markdown({ content }: MarkdownProps) {
  const { theme } = useTheme();
  const isDark = theme === "dark";

  return (
    <ReactMarkdown
      components={{
        h1: (props) => <h1 className="text-2xl font-bold my-4" {...props} />,
        h2: (props) => <h2 className="text-xl font-bold my-3" {...props} />,
        h3: (props) => <h3 className="text-lg font-bold my-2" {...props} />,
        p: (props) => <p className="my-2" {...props} />,
        ul: (props) => <ul className="list-disc pl-5 my-2" {...props} />,
        ol: (props) => <ol className="list-decimal pl-5 my-2" {...props} />,
        li: (props) => <li className="my-1" {...props} />,
        strong: (props) => <strong className="font-bold" {...props} />,
        em: (props) => <em className="italic" {...props} />,
        blockquote: (props) => (
          <blockquote
            className={`border-l-4 ${
              isDark ? "border-gray-700" : "border-gray-200"
            } pl-4 my-2 italic`}
            {...props}
          />
        ),
        code: ({
          inline,
          ...props
        }: { inline?: boolean } & React.HTMLAttributes<HTMLElement>) =>
          inline ? (
            <code
              className={`${
                isDark ? "bg-gray-800" : "bg-gray-100"
              } px-1 py-0.5 rounded`}
              {...props}
            />
          ) : (
            <code
              className={`block ${
                isDark ? "bg-gray-800" : "bg-gray-100"
              } p-2 rounded my-2 overflow-x-auto`}
              {...props}
            />
          ),
        hr: () => (
          <hr
            className={`my-4 border-t ${
              isDark ? "border-gray-700" : "border-gray-300"
            }`}
          />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}
