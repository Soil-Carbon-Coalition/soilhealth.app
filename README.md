SOILHEALTH.APP project notes

Back end for an open-source offline-capable web app for a shared, participatory, evidence-based local intelligence on soil health, watershed function, and economic function. See [soilcarboncoalition.org/atlas] and [soilhealth.app] for an overview of the direction and design.

This project is a reconfiguration of the back end of atlasbiowork.com, with the major addition of a Project model, whereby projects can be adaptively configured with their own observation templates.

Users will register, ask a local Project Coordinator (who has admin privileges) for permission to join a project as an Observer. Once joined, they will be able to enter new sites (point or polygon) and record observations for that site and project, and view results on interactive maps.

Django apps include:

obs - the main Observation app. Model uses Postgres JSON field for data as well as data entry templates.

maps - these can be multilayered mashups of raster and vector layers rendered in Leaflet.

The front end is in Vue.js ([https://github.com/Soil-Carbon-Coalition/vueapp])
