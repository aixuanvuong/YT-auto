instances=(
  "https://pipedapi.kavin.rocks"
  "https://pipedapi.moomoo.me"
  "https://pipedapi.syncpundit.io"
  "https://pipedapi.us.projectsegfau.lt"
  "https://piped-api.lunar.icu"
  "https://api.piped.privacydev.net"
  "https://pipedapi.smnz.de"
  "https://pipedapi.adminforge.de"
  "https://pipedapi.qwik.space"
  "https://ytapi.drgns.space"
)

for url in "${instances[@]}"; do
  echo "Testing $url..."
  res=$(curl -sL "$url/search?q=test&filter=all" | head -c 50)
  echo "Result: $res"
done
