#!/usr/bin/env bash

npm install
npm run build -- --base-href=/ui/ --configuration=${UI_BUILD_CONFIGURATION}
