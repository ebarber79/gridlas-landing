# GitHub push via VPS relay (why `git push` works from this Pi)

## The problem
This Pi's network egress BLOCKS GitHub's IP ranges entirely — GitHub's ASN
(140.82.x), its Azure range (20.x), and GitHub Pages (185.199.108-111.153,
which is what gridlas.com itself resolves to). Every port (22/443) times out.
The rest of the internet works fine, including GitHub's Fastly CDN
(raw.githubusercontent.com). It's an upstream egress policy, not fixable on the Pi.

## The fix (transparent — plain `git push` just works)
`~/.ssh/config` routes github.com SSH through the IONOS VPS on Tailscale
(my-vps-ionos, 100.93.253.90), which CAN reach GitHub. The relevant block:

    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_ed25519
        ProxyCommand ssh -o BatchMode=yes -W %h:%p root@100.93.253.90
        ...

GitHub authentication (the ed25519 key) happens END-TO-END from this Pi.
The VPS only relays the encrypted TCP stream — it never sees GitHub creds.

## Requirements for it to work
- Tailscale up on this Pi AND the VPS (100.93.253.90 must show online/active)
- Passwordless SSH from Pi -> root@100.93.253.90 (Tailscale + key)
- The VPS's own egress can reach github.com:22

## If push ever fails
1. `tailscale status | grep 100.93.253.90`  -> must be online/active
2. `ssh root@100.93.253.90 'echo ok'`        -> must return ok, no password
3. `ssh root@100.93.253.90 'timeout 6 bash -c "exec 3<>/dev/tcp/140.82.112.3/22" && echo gh-ok'`
4. Temporary manual override if config is lost:
   git -c core.sshCommand="ssh -o ProxyCommand='ssh -W %h:%p root@100.93.253.90'" push origin main

## Real fix (someday)
Get the network egress policy to allow GitHub IP ranges, then remove the
`Host github.com` block from ~/.ssh/config. Until then, the relay is the path.
