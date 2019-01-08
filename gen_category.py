categories = [
    ("misc", "Miscellaneous"),
    ("japanese", "Japanese"),
    ("javascript", "Javascript"),
    ("elixir", "Elixir"),
    ("til", "Today I Learned"),
    ("ecto", "Ecto"),
    ("game", "Game"),
    ("phaserjs", "Phaser JS"),
    ("security", "Security"),
    ("web", "Web"),
    ("ctf", "Capture The Flag"),
    ("unicode", "Unicode"),
    ("blockchain", "Blockchain"),
    ("ethereum", "Ethereum"),
    ("smartcontract", "Smart Contract"),
    ("phoenix", "Phoenix"),
    ("websocket", "Websocket"),
]

template = """---
layout: posts_by_category
categories: %s
title: %s
permalink: /category/%s
---"""


for slug, title in categories:
    with open("category/%s.md" % slug, "w") as f:
        content = template % (slug, title, slug)
        f.write(content)
