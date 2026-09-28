source_id: STREAMLIT_CACHE
title: Streamlit Caching Overview
url: https://docs.streamlit.io/develop/concepts/architecture/caching

Streamlit caching avoids repeating expensive work on every rerun. st.cache_data is designed for data results that can be serialized and copied, while st.cache_resource is designed for shared resources such as models or database connections. Time-to-live settings can control cache invalidation.
