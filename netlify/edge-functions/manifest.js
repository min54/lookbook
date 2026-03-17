export default async (request) => {
    const host = new URL(request.url).hostname;

    // Supabase에서 도메인 일치하는 매장 이름 조회
    let shopName = 'D-lookbook';
    try {
        const res = await fetch(
            'https://cdqstqlpaihvexbmjdfd.supabase.co/rest/v1/shops?select=name,domain',
            {
                headers: {
                    apikey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkcXN0cWxwYWlodmV4Ym1qZGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NDQ1NDQsImV4cCI6MjA4OTIyMDU0NH0.4c-ROHG1Qy0s5JPHuBgPpOxbE_j1EljDDswBlTe7NaM',
                    Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNkcXN0cWxwYWlodmV4Ym1qZGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NDQ1NDQsImV4cCI6MjA4OTIyMDU0NH0.4c-ROHG1Qy0s5JPHuBgPpOxbE_j1EljDDswBlTe7NaM',
                }
            }
        );
        const shops = await res.json();
        const matched = shops?.find(s => {
            if (!s.domain) return false;
            try {
                const h = new URL(s.domain.includes('://') ? s.domain : 'https://' + s.domain).hostname;
                return h === host;
            } catch { return s.domain.includes(host); }
        });
        if (matched) shopName = matched.name;
    } catch (_) {}

    const manifest = {
        name: shopName + ' Dress Collection',
        short_name: shopName,
        display: 'fullscreen',
        display_override: ['fullscreen', 'standalone'],
        background_color: '#0a0a0a',
        theme_color: '#0a0a0a',
        start_url: '/',
        icons: [
            { src: 'icons/icon-192.svg', sizes: '192x192', type: 'image/svg+xml', purpose: 'any maskable' },
            { src: 'icons/icon-512.svg', sizes: '512x512', type: 'image/svg+xml', purpose: 'any maskable' }
        ]
    };

    return new Response(JSON.stringify(manifest), {
        headers: { 'Content-Type': 'application/manifest+json' }
    });
};

export const config = { path: '/manifest.json' };
