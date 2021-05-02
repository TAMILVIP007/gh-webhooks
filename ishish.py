import re
import traceback
from datetime import datetime
from html import escape

import github
from aiohttp import web
from decouple import config
from telethon import Button, events

from client import tgbot

BOT_TOKEN = config("TOKEN")
# from flask import Flask, request, Response
print("Go Injoi!")
"""API = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def post_tg(chat, message, parse_mode):
    # Send message to desired group
    response = requests.post(
        API + "sendMessage",
        params={
            "chat_id": chat,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        },
    ).json()
    return response"""


def better_time(text):
    try:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    except ValueError:
        cr_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S+05:30")
        cr_time = cr_date.strftime("%m/%d/%Y %H:%M")
    return cr_time


g = github.Github()


@tgbot.on(events.CallbackQuery(pattern="stars_count"))
async def callback(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    stars = repo.stargazers_count
    await event.answer(f"Total 🌟Stars🌟 are {stars}.", alert=True)


@tgbot.on(events.CallbackQuery(pattern="forks_count"))
async def fucku(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    forks = repo.forks_count
    await event.answer(f"Total Forks are {forks} ⚡️.", alert=True)


@tgbot.on(events.CallbackQuery(pattern="pr_count"))
async def pcount(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    open_pr_count = 0
    closed_pr_count = 0
    total_prs = 0
    for r in repo.get_pulls(state="open"):
        open_pr_count += 1
    for r in repo.get_pulls(state="closed"):
        open_pr_count += 1
    for r in repo.get_pulls(state="all"):
        total_prs += 1
    await event.answer(
        f"Total Open Pull Requests are {open_pr_count}.\nTotal Closed Pull Requests are {closed_pr_count}\n\nTotal Pull Requests are {total_prs}",
        alert=True,
    )


@tgbot.on(events.CallbackQuery(pattern="issue_count"))
async def pcount(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    issue_count = 0
    for r in repo.get_issues(state="open"):
        issue_count += 1
    await event.answer(f"Total Open Issues are: {issue_count}", alert=True)


@tgbot.on(events.NewMessage(pattern="^/stats", func=lambda e: e.is_private))
@tgbot.on(
    event.NewMessage(pattern="^/stats@CyberneticistBot", func=lambda e: e.is_group)
)
async def fucku(event):
    repo = g.get_repo("TeamUltroid/Ultroid")
    desc = repo.description
    lang = repo.language
    last_c = repo.last_modified
    watchers = repo.watchers_count
    repo.get_license().license.name
    text = f"**Ultroid Userbot Stats**\n\n**Repo:** [Ultroid]({repo.html_url})\n**Description:** {desc}\n**Last Updated:** {last_c}\n**Language:** {lang}\n**Watchers:** {watchers}\n\n**License:** {license}"
    btns = [
        [
            Button.inline("🌟Stars🌟", b"stars_count"),
            Button.inline("🍴Forks", b"forks_count"),
        ],
        [
            Button.inline("Pull Requests", b"pr_count"),
            Button.inline("Issues", b"issue_count"),
        ],
    ]
    await event.send_message(event.chat_id, text, buttons=btns)


async def respond(request):
    result = await request.json()
    #    await tgbot.start(bot_token=BOT_TOKEN)
    # print(request.json)
    d_form = "%d/%m/%y || %H:%M"

    @tgbot.on(events.CallbackQuery(pattern="stars"))
    async def callback(event):
        total_stars = result["repository"]["stargazers_count"]
        await event.answer(f"Total 🌟Stars🌟 are now {total_stars} .", alert=True)

    @tgbot.on(events.CallbackQuery(pattern="forks"))
    async def fucku(event):
        total_forks = result["repository"]["forks_count"]
        await event.answer(f"Total Forks are {total_forks} ⚡️ .", alert=True)

    try:
        # check_s = result["check_suite"]
        # umm = check_s["app"]["head_commit"]
        if result.get("commits"):
            commits_text = ""

            rng = len(result["commits"])
            if rng > 10:
                rng = 10
            for x in range(rng):
                commit = result["commits"][x]
                pull_ts = commit["timestamp"]
                str_time = better_time(pull_ts)
                commit_url = commit["url"]
                strr = commit["author"]["email"]
                Commiter = ""
                if re.search("noreply.github.com", strr):
                    strss = strr.split("+")
                    for i, w in enumerate(strss):
                        fk = w.split("@")[0]
                        Commiter += fk
                elif commit["author"]["username"]:
                    Commiter += commit["author"]["username"]
                else:
                    users = g.search_users(commit["author"]["email"])
                    for user in users:
                        Commiter += user.login

                if len(escape(commit["message"])) > 300:
                    commit_msg = escape((commit["message"]).split("\n")[0])
                else:
                    commit_msg = commit["message"]

                btns = [
                    (
                        Button.url("View Commit", f"{str(commit_url)}"),
                        Button.url(
                            "Commited By",
                            f"https://github.com/{Commiter}",
                        ),
                    )
                ]
                if len(commits_text) > 1000:
                    commits_text += f"{commit_msg}\n<a href='{commit['url']}'>{commit['id'][:7]}</a> by {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
                    text = f"""✨ <b>{escape(result['repository']['name'])}</b> : New {len(result['commits'])} commits on {escape(result['ref'].split('/')[-1])} branch
{commits_text}#Github"""
                    response = await tgbot.send_message(
                        -1001237141420, text, parse_mode="html", link_preview=False
                    )
                    print(response)
                else:
                    commits_text += f"{commit_msg}\n{commit['id'][:7]} by {commit['author']['name']} {escape('<')}{commit['author']['email']}{escape('>')}\n\n"
                    text = f"""✨ <b>{escape(result['repository']['name'])}</b> : New {len(result['commits'])} commits to {escape(result['ref'].split('/')[-1])} branch
{commits_text}#Github"""
                    commit["url"]
                    response = await tgbot.send_message(
                        -1001237141420,
                        text,
                        parse_mode="html",
                        buttons=btns,
                        link_preview=False,
                    )
                    print(response)
        elif result.get("pull_request"):
            pr_action = result["action"]
            pr = result["pull_request"]
            pull_r = pr["html_url"]
            pull_t = pr["title"]
            pr["body"]
            pull_commits = pr["commits_url"]
            pull_ts = pr["created_at"]
            str_time = better_time(pull_ts)
            pull_pusher = pr["user"]["login"]
            if pr_action == "opened":
                text = f"**Opened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#Github"
            elif pr_action == "closed":
                text = f"**Closed Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#Github"
            else:
                text = f"**Reopened Pull Request**\nBy: {pull_pusher}\n[{pull_t}]({pull_r})\n**Timestamp**: {str_time}\n[Commits]({pull_commits})\n\n#Github"
            await tgbot.send_message(
                -1001237141420, text, parse_mode="markdown", link_preview=False
            )
        elif result.get("action") == "started":
            repo_name = result["repository"]["name"]
            repo_url = result["repository"]["html_url"]
            stargiver_uname = result["sender"]["login"]
            stargiver_profile = result["sender"]["html_url"]
            result["repository"]["stargazers_count"]
            text = f"🌟 [{stargiver_uname}]({stargiver_profile}) starred [{repo_name}]({repo_url}).\n\n#Github"
            await tgbot.send_message(
                -1001237141420,
                text,
                parse_mode="markdown",
                buttons=Button.inline("Total Stars", b"stars"),
                link_preview=False,
            )
        elif result.get("forkee"):
            repo_n = str(result["repository"]["name"])
            repo_url = str(result["repository"]["html_url"])
            forker_u = str(result["sender"]["login"])
            forker_p = str(result["sender"]["html_url"])
            text = f"""🍴[{forker_u}]({forker_p}) **forked** [{repo_n}]({repo_url})\n\n#Github"""
            await tgbot.send_message(
                -1001237141420,
                text,
                parse_mode="markdown",
                buttons=Button.inline("Total Forks", b"forks"),
                link_preview=False,
            )
        else:
            return
            # IDK WHat
            # loop.run_until_complete()
    except BaseException:
        traceback.print_exc()


PORT = config("PORT")
if __name__ == "__main__":
    app = web.Application()
    app.router.add_route("POST", "/webhook", respond)
    web.run_app(app, port=PORT)
