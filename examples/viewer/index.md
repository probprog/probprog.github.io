---
title: Examples
layout: worksheet
---

<!--
  ~ This file is part of gorilla-repl. Copyright (C) 2014-, Jony Hudson.
  ~
  ~ gorilla-repl is licenced to you under the MIT licence. See the file LICENCE.txt for full details.
  -->

<div id="contents" data-bind="css: {veiled: copyBoxVisible}">
    <div class="segment container-segment">
        <div class="container-children">
            <div data-bind="template: {name: 'segment-template', foreach: worksheet().segments()}">
            </div>
        </div>
    </div>
</div>

<div class="scroll-pad"></div>

<!-- Templates -->
<script type="text/html" id="segment-template">
    <div data-bind="template: {name: renderTemplate}"></div>
</script>

<script type="text/html" id="code-segment-template">
    <div class="segment code">

        <div class="segment-main">
            <pre class="static-code clojure"><code data-bind="text: contents"></code></pre>
        </div>
        <div class="error-text" data-bind="text: errorText, visible: errorText() !== ''"></div>
        <div class="console-text" data-bind="visible: consoleText() !== ''">
            <pre><code data-bind="html: consoleText"></code></pre>
        </div>
        <div class="output"
             data-bind="visible: (output() != ''), outputViewer: output, segmentID: id">
        </div>
        <div class="segment-footer"></div>
    </div>
</script>

<script type="text/html" id="free-segment-template">
    <div class="segment free">
        <div class="segment-main">
            <div class="free-preview" data-bind="mathJaxViewer: renderedContent"></div>
        </div>
        <div class="segment-footer"></div>
    </div>
</script>
