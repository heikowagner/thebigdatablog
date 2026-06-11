---
categories:
- All Articles
- Introduction
date: '2022-01-12'
slug: a-wordpress-plugin-to-embed-raw-githubusercontent
status: publish
tags: []
title: A WordPress Plugin to embed raw.githubusercontent
wp_id: 3120
wp_modified: '2023-10-01T10:11:08'
---

Working at my post [about the dask cluster](https://www.thebigdatablog.com/building-a-minimal-cost-efficient-dask-cluster/), I realized that the code snippets presented in the post will eventually change in my GitHub Repo. I wanted to avoid having to make all the changes manually. Therefore, I was looking for a method to automatically include the code for the scripts. Optimally while retaining the code highlighting using  [SyntaxHighlighter Evolved by Alex Mills](https://wordpress.org/plugins/syntaxhighlighter/). As a quick Google search turns out, there is nothing out there so far. Thus I decided to do the implementation myself.

Basically I just took the code of Alex Mills and wrapped it into a plugin. However that was not enough, since WordPress do not support nested shortcodes. However, there is a way to realize nested shortcodes using the [do\_shortcode()](https://developer.wordpress.org/reference/functions/do_shortcode/) function. Since the SytaxHighlighter does not use this function, I added a filter to apply the function to all the\_content objects using the add\_filter() function. add\_filter() has a $priority variable, which controls when the filter is applied. Since we modify all the\_content choosing a small number here might break your WordPress installation. After taking a look in the [SyntaxHighlighter Code](https://github.com/Automattic/syntaxhighlighter/blob/master/syntaxhighlighter.php) I realized that going with priority=9 is a suitable choice. \
\
To Install the Plugin, [download Plugin](https://github.com/heikowagner/load_external_script/archive/refs/tags/1.0.zip) and install using “Plugins ->New Plugin->Upload”.