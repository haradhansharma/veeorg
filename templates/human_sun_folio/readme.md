---
title: "Human Sun Folio HTML Template Using Bootstrap 5.3"
author : Haradhan Sharma
date: April 2, 2024
description: "Welcome to the Human Sun Folio HTML Template - a sleek, clean, and elegant design crafted with Bootstrap 5.3.1. This interactive template is easily integrated with HTMX, Django, Laravel, or any other framework that supports HTML templates."
---

# Human Sun Folio HTML Template Using Bootstrap 5.3

Welcome to the Human Sun Folio HTML Template - a sleek, clean, and elegant design crafted with Bootstrap 5.3.1. This interactive template is easily integrated with HTMX, Django, Laravel, or any other framework that supports HTML templates.

## Features
- Responsive Design: All pages feature a responsive font size and page indicators. Fit with all device screen.
- Interactive Elements: Selected divs have elegant mouse interactions with MagicMouse JS.
- Custom Scrollbars: Enhanced browsing experience with OverlayScrollbars JS.
- Sticky Navbar: Includes a mega menu for easy navigation.
- Bright and Branded: The template crafted with completely branded colors in bright tone.
- Branding & Footer: A clean and branded header and footer with a meaningfull 'Go to Top' button.
- Megamenu: Expandable menu items with custom scrollbars and introductory section. Menu Open from top covering full page.
- Front Page: Showcases the portfolio creator with sections for self-branding, experience, skills, and more.
- Contact Page: Includes a form and Google Map embed integration along with contact info and animated placeholders.
- About Page: Offers a detailed overview and buttos for printing the page as a CV/resume.
- Blog Pages: Contains a list of blogs with a search function, pagination, and clean layout.
- Blog Details: Styled elements for blog content, including blockquotes, code snippets, and lists. Social sharing buttons and comment section included.
- Additional Templates: Projects & Project Details templates, Service & Service Details templates, and error pages (403, 404, 500).
- Glitbox Gallery for Project Overview in Project Detail page.
- SVG logo and icons. Can be integrate with lottie animation as well.
- Completely depends on Bootstrap 5.3 except some below consideration.
- Optimized minified image with loader.
- Facebook like and share area defined in blogs details, roject details page template.
- Sample `ads.txt` and `robot.txt` Included
- PWA optimized with `manifest.json`.
- `sitemap.xml` implemented.


## Customization
- Use `main.js` and `style.css` for further customization.
- Font size classes: `fs-1x`, `fs-1xx`, `fs-8vw`.
- Height classes: `vh-75`, `min-vh-75`.
- Content heading classes: `blog-section-heading`, `side-block-title`.
- Use `specialeffect` or `specialeffectImage` along with `magic-hover` class to extend magic mouse behavior. Follow exmple implementation in `main.js`.
- Use `cardeffectEx` class to add MagicMouse effect of DIVs.
- Use `#applyScrolbar` by following OverlayScrollbarsJS docuemntation
- glitbox demand some cutomiztion to incorporate with MagicMouse. Follow the implmetation in JS file.
- `marqueeContainer{i}` with left or right direction used to call `setupMarquee('marqueeContainer', 'left');` in skills section. Follow the example to implement.

## Dependencies
- jQuery v3.6.4(Included)
- AOS js(Included)
- animate.css(Included)
- animate.css(CDN used, This extended external library Needed)
- Bootstrap 5.3(Included)
- Line-awesome(Included)
- Simple-line-icons(Included)
- OverlayScrollbars js (CDN used)
- Vivus JS(CDN Used)
- MagicMouse JS(CDN used)
- GlitBox JS(CDN used)
- `Aldrich` font included

## Optimization & Extras
- PWA optimized with manifest included.
- SEO optimized skeleton.
- Includes blank ads.txt and robots.txt files.
- sitemap.xml provided.
- Default font "Aldrich" is implemented; additional icon fonts are in the fonts folder.

## Implementation Notes
- For adding Lottie animations, follow the Lottie Player documentation including JS or CDN (not implemented in this template by default).
- For adding HTMX , follow the HTMX documentation including (not implemented in this template by default).
- To Implement with Django, please contact with Haradhan Sharma to get paid support.
- To customize fonts and colors, modify `main.js` and `style.css`. For custom color themeing modify carefully `bs-theme-overrides.css`.
- If the preloader is not desired, add `d-none` to the "#loader" element at the top and comment `callLoader()` from the `main.js`.
- You are free to play with included JS with caution. Please reffer to the designated documentation of specific JS library. 
- Use `printButton` class to create custom print button in any page. But follow the guideline to decorate print page of bootstrap 5.3.
- By default `d-print-none` applied to the navbar, footer and mega menu. So those will not print on windows print. 
- Edit css to add image in loader, but caution with size to reduce load time.
- No API key is required to add google map in contact page. Just embed by following guideline aviable with google.
- go back button implemented in each page's content section with 'X' icon to go to the reffeer page using JS. You can adjust it as per your requirements.

## How to Use
- Megamenu & Navbar: Customize the text to introduce the portfolio creator and add personal contact information.
- Front Page: Update the self-branding sections with your details and imagery.
- Contact Form: Configure the form to connect to your backend or service of choice.
- About Page: Fill in your professional overview and details.
- Blogs: Use the provided skeletons to add your content.
- Additional Pages: Modify the project and service single page and detail page templates as needed.

## Support
- To implement this template with django please write to Haradhan Sharma
