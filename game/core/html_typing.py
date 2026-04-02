# Helper functions for HTML-safe typing effects.
# This keeps TypingTextBox focused on UI behavior and makes the logic reusable.

# Also to make sure UI doesn't become a 20000000 line file lol


# TODO: Cache parsed tag positions if we ever need to optimize for long texts.


def visible_text_length(html_text):
    in_tag = False
    count = 0
    for ch in html_text:
        if ch == "<":
            in_tag = True
            continue
        if ch == ">":
            in_tag = False
            continue
        if not in_tag:
            count += 1
    return count


def truncate_html(html_text, visible_chars):
    # Keep tags intact while revealing only visible characters.
    out = []
    tag = []
    in_tag = False
    count = 0
    open_tags = []

    i = 0
    while i < len(html_text) and count < visible_chars:
        ch = html_text[i]
        if ch == "<":
            in_tag = True
            tag = ["<"]
        elif ch == ">" and in_tag:
            tag.append(">")
            tag_str = "".join(tag)
            out.append(tag_str)
            in_tag = False
            tag_name = _tag_name(tag_str)
            if tag_name:
                if tag_str.startswith("</"):
                    if open_tags and open_tags[-1] == tag_name:
                        open_tags.pop()
                elif not tag_str.endswith("/>"):
                    open_tags.append(tag_name)
        else:
            if in_tag:
                tag.append(ch)
            else:
                out.append(ch)
                count += 1
        i += 1

    while open_tags:
        out.append(f"</{open_tags.pop()}>")
    return "".join(out)


def _tag_name(tag_str):
    # TODO: Clean and make it pretty, this is very rough :(
    if not tag_str.startswith("<") or not tag_str.endswith(">"):
        return None
    if tag_str.startswith("</"):
        inner = tag_str[2:-1].strip()
    else:
        inner = tag_str[1:-1].strip()
    if not inner or inner.startswith("!"):
        return None
    return inner.split()[0].strip("/")
