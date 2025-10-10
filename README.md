©2025 The MITRE Corporation. ALL RIGHTS RESERVED.
 
The author's affiliation with The MITRE Corporation is provided for identification purposes only, and is not intended to convey or imply MITRE's concurrence with, or support for, the positions, opinions, or viewpoints expressed by the author.'©2025 The MITRE Corporation. ALL RIGHTS RESERVED.
NOTICE
 
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software Documentation Clause 252.227-7014 (FEB 2014)


# Introduction 
Graphex plugin enabling web automation.

# Installation
Install the plugin with the command `make all`. This also sets up the required Playwright tools for automation.

# Execution
This repository is not intended for standalone use. It bridges the gap between Python's Playwright web automation tool and the Graphex module.

# Using Playwright Nodes

The `graphex_webautomation_plugin` leverages the [Playwright](https://playwright.dev/) Python package by Microsoft. This open-source tool automates browser interactions with Chromium, Firefox, and WebKit in Python, among other languages. A standout feature is Playwright's code generation tool, simplifying browser interaction scripting.

## Interacting with the Browser

The `Create Playwright Browser Context` node initiates a browser context, akin to manually opening a new browser window. Multiple pages can be opened within this context.

![image](./.images/create_page.png)

For clarity: manually launching a browser and logging into a site means you won't need to log in again when opening a new tab in that browser. This is due to session retention (usually via cookies). Likewise, Playwright's browser context maintains session data across its pages, so actions like logging in on one page are recognized on others within the same context.


## Crafting and Executing Page Commands

The `Execute Playwright Page Script` node allows synchronous execution of a series of Playwright commands in Python. The node accepts a `page commands` script which has access to these local variables:

- **page**: A `playwright.sync_api.Page` python object
- **output**: A data container that can be a list or a dictionary, used for storing parsed outputs
- **re**: the standard regex library
- **time**: the standard time library

The `Execute Playwright Page Script` node facilitates the synchronous execution of a series of Playwright commands in Python. It accepts a `page commands` script, which can access the following local variables:

- **page**: A `playwright.sync_api.Page` object
- **output**: A container, either a list or a dictionary, for storing parsed outputs
- **re**: The standard regex library
- **time**: The standard time library

For example, to download the Ubuntu 22.04.3 desktop iso, use:

```python
page.goto("https://ubuntu.com/download/desktop")
page.get_by_role("button", name="Accept all and visit site").click()
page.get_by_role("link", name="Search Search").click()
page.get_by_placeholder("Search our sites").fill("22.04.3")
page.get_by_placeholder("Search our sites").press("Enter")
page.get_by_role("link", name="Ubuntu 22.04.3 LTS (Jammy Jellyfish)", exact=True).click()
with page.expect_download() as download_info:
    page.get_by_role("link", name="64-bit PC (AMD64) desktop image").click()
download = download_info.value
```

By default, the plugin waits up to 30 seconds for an element's appearance before erroring out. No need for explicit timeouts. Adjust this duration using the `Element Timeout (ms)` option in the `Open a Playwright Page` node. The plugin handles file downloads automatically, storing their paths in the `Download Filepaths` output.

## Creating Page Commands

To use Playwright's code generation tool for creating page commands, follow these steps:

1. Install playwright: `pip install playwright`.
2. Set it up: `python3 -m playwright install`.

Use the codegen tool while bypassing HTTPS errors with:

```bash
python3 -m playwright codegen --ignore-https-errors --viewport "1920, 1080"
```

This command launches a Chromium browser alongside Playwright's code generator. Interact with the browser, and it'll log commands for you.

![image](./.images/cats.png)

For the `Execute Playwright Page Script` node, extract commands post `goto` (assuming a predefined URL):

![image](./.images/playwright_codegen_example.png)

Then, input the code block into the node's `page_commands`.

## Refining Codegen Commands

While Playwright's Python codegen tool is an excellent starting point for web automation, always review the auto-generated code. Here are points to consider:

1. **Is the selector overly specific?** 
   
    Avoid relying on hardcoded values, like specific version numbers. For instance, while automating the task of navigating to the Express NPM package page and selecting the latest version:

    ![image](./.images/npm_example.png)
    
    As of october 2023, playwright codegen will produce this code:

    ```python
    page.goto("https://www.npmjs.com/package/express?activeTab=versions")
    page.locator("li").filter(has_text="4.18.217,767,703latest").get_by_label("4.18.2").click()
    ```

    This code becomes obsolete when the version updates. Here's the HTML structure from the browser's inspect tool for clarity:

    ```html
    <li>
        <a href="/package/express/v/4.18.2" aria-label="4.18.2">4.18.2</a>
        <div>17,767,703 downloads</div>
        <div class="latest-tag">latest</div>
    </li>
    ```

    Given this structure, you'd want to target the `li` with the text "latest" and its child `a` element:

    ```python
    page.locator('li', has_text='latest').locator('a').click()
    ```

    Now the commands will work if the version is updated.

2. **Does it handle delayed actions?**

    Playwright might not always detect delayed actions like downloads. To handle such scenarios, use constructs like `page.wait_for_event("download")`. For example, if there's a missed 'with' context for a download:

    ```python
    page.get_by_role("link", name="64-bit PC (AMD64) desktop image").click()
    ```

    Modify it to:

    ```python
    with page.expect_download() as download_info:
        page.get_by_role("link", name="64-bit PC (AMD64) desktop image").click()
    download = download_info.value
    ```

By carefully reviewing and refining the codegen's output, your automation becomes more efficient and adaptable to web content changes.

# Advanced Playwright Nodes

Web automation, particularly with tools as advanced as Playwright, offers an array of features that often go unnoticed by many. To truly harness the power of the `graphex_webautomation_plugin` and Playwright, it's crucial to delve deeper into the advanced nodes the plugin provides. A deeper understanding the playwright framework can be found [here](https://playwright.dev/python/docs/api/class-playwright).

## Locators

The essence of any web automation task lies in the ability to pinpoint and interact with specific elements on a web page. Playwright streamlines this task using 'locators'.

### What is a Locator?

A locator in Playwright can be visualized as a guiding beacon that directs your automation script to the desired element(s) on a page. Instead of manually sifting through the webpage's code to identify the unique identifiers or attributes, locators enable you to set a criteria and allow Playwright to handle the element selection.

### Using Get By Role

The `get_by_role` function in Playwright fetches elements based on their ARIA roles, making it particularly useful for targeting specific accessibility roles on web pages.

Examples:

- **Fetching a button**:
   Suppose you have a webpage with buttons that says "Hover":

   ![image](./.images/button_example_pure.png)
   
  To target these buttons, we can use the following nodes:
   
   ![image](./.images/button_example.png)
   
   This graph fetches the buttons based on its role and name (which is typically its accessible label). In this case all 'Hover' buttons are selected.

- **Fetching all links**:
   Suppose instead we want to target all links on a page:

  ![image](./.images/link_example_pure.png)

  The following nodes well target all links:

  ![image](./.images/get_link_graph.png)

  This graph fetches all links found on the page.
   

## Filters

In many cases, merely locating an element isn't enough. You might encounter scenarios where you need to fine-tune your selection. This is where filters come into play.

### Working with Filters

Building on the locator's capabilities, filters refine the results to better match the desired criteria. Filters are invaluable when:

- Elements share common attributes, and you need to select a specific one.
- Your automation task requires dynamic selection based on content rather than attributes.

For instance, if you've used a locator to select all links on a page but only wish to interact with those containing a specific pattern, a regex filter can achieve this.

Example:

Lets say we want to click the link with text `a text link`:

![image](./.images/page_link_example.png)

We can use the following graph to find all links and filter to this exact name via regex:

![image](./.images/Filter_By_Regex.png)


In the above code, the locator fetches all anchor (`a`) tags, but the filter refines the selection to only those containing the exact match "a text link".

## Actions

Once you've honed in on the target element(s) using locators and filters, actions breathe life into your automation script. With locators pinpointing the exact location, actions dictate what to do next.

### Common Actions

- **Click**: Interact with clickable elements like buttons, links, etc.
  
  Example: Suppose we want to click this first 'Hover' button on a page:

  ![image](./.images/button_example_pure.png)


  The following graph will search for all buttons named 'Hover' and click the first one.

  ![image](./.images/click_example_graph.png)

  After this graph is executed the first element will be clicked.

  ![image](./.images/click_example.png)


- **Fill**: Enter text into input fields.

  Example: Suppose we want to fill in the 'Text Input label' input:

  ![image](./.images/pre_fill_example.png)

  We can do so with the following graph:

  ![image](./.images/fill_graph_example.png)

  This graph will locate the input element by label and fill it with the appropriate text.

  ![image](./.images/post_fill_example.png)

- **Screenshot**: Capture visual state of an element or entire page.

  Screenshots of the browser can be logged for easy debugging. Using the fill example above, we can capture the browser screen before and after inputing the text with the following graph.

  ![image](./.images/screen_shot_example.png)
  

By chaining locators, filters, and actions, you can construct powerful automation sequences that navigate, interact with, and even adapt to the dynamic content of modern webpages. This trifecta forms the bedrock of advanced web automation with Playwright in the `graphex_webautomation_plugin`.





