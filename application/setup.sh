mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"mica2014@comcast.net\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml