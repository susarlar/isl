// Minimal safe markdown renderer.
// Escapes HTML first so user/model output cannot inject tags, then applies
// a small subset of markdown: headers, bold, italic, inline code, lists,
// blockquotes, code blocks, and paragraph/line breaks.
//
// This is intentionally NOT a full markdown parser — it's scoped to what the
// Fellow Power Advisor LLM actually emits.
window.renderMarkdown = function (raw) {
    if (!raw) return "";

    const escape = (s) =>
        s
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");

    let text = escape(String(raw));

    // Fenced code blocks ```...```
    text = text.replace(/```([\s\S]*?)```/g, (_, code) =>
        "<pre><code>" + code.replace(/\n/g, "&#10;") + "</code></pre>"
    );

    // Inline code `...`
    text = text.replace(/`([^`\n]+)`/g, "<code>$1</code>");

    // Headers (at line start). Process h6 → h1 so longer # runs win.
    text = text.replace(/^######\s+(.+)$/gm, "<h6>$1</h6>");
    text = text.replace(/^#####\s+(.+)$/gm, "<h5>$1</h5>");
    text = text.replace(/^####\s+(.+)$/gm, "<h4>$1</h4>");
    text = text.replace(/^###\s+(.+)$/gm, "<h3>$1</h3>");
    text = text.replace(/^##\s+(.+)$/gm, "<h2>$1</h2>");
    text = text.replace(/^#\s+(.+)$/gm, "<h1>$1</h1>");

    // Bold **text** — process before italic so ** doesn't get eaten as *
    text = text.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");

    // Italic *text* (not matching ** already consumed)
    text = text.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");

    // Blockquotes: > line
    text = text.replace(/^&gt;\s?(.*)$/gm, "<blockquote>$1</blockquote>");

    // List items — mark unordered and ordered separately so we can emit
    // <ul> vs <ol> correctly at wrap time.
    text = text.replace(/^[\-*]\s+(.+)$/gm, "\u0001ULI\u0001$1\u0002");
    text = text.replace(/^\d+\.\s+(.+)$/gm, "\u0001OLI\u0001$1\u0002");

    // Wrap consecutive ULI markers in <ul>, OLI in <ol>.
    text = text.replace(/(\u0001ULI\u0001[^\u0002]*\u0002(?:\s*\u0001ULI\u0001[^\u0002]*\u0002)*)/g, (group) =>
        "<ul>" + group.replace(/\u0001ULI\u0001([^\u0002]*)\u0002/g, "<li>$1</li>") + "</ul>"
    );
    text = text.replace(/(\u0001OLI\u0001[^\u0002]*\u0002(?:\s*\u0001OLI\u0001[^\u0002]*\u0002)*)/g, (group) =>
        "<ol>" + group.replace(/\u0001OLI\u0001([^\u0002]*)\u0002/g, "<li>$1</li>") + "</ol>"
    );

    // Paragraph / line break handling. Split on blank lines for paragraphs,
    // single newlines become <br> inside a paragraph. Skip wrapping block
    // elements we already produced.
    const blocks = text.split(/\n{2,}/);
    const wrapped = blocks.map((block) => {
        const trimmed = block.trim();
        if (!trimmed) return "";
        if (/^<(h\d|ul|ol|pre|blockquote)/.test(trimmed)) {
            return trimmed;
        }
        return "<p>" + trimmed.replace(/\n/g, "<br>") + "</p>";
    });

    return wrapped.join("\n");
};
