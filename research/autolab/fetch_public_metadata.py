"""Read public task metadata, using an existing AutoLab login if required.

This script only performs GET requests and writes public task/image metadata.
It never saves or prints credentials. Run with AutoLab's Python environment.
"""
import asyncio
import json
from pathlib import Path
from urllib.request import Request, urlopen

from autolab.cli import _client_at

OUT = Path(__file__).resolve().parent
IMAGE_DIGEST = "sha256:964547ad81e109c78545512867bae70b710c55d833078674878faad7de0ebb85"


def get_json(url, headers=None):
    with urlopen(Request(url, headers=headers or {})) as response:
        return json.load(response)


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + "\n")


async def main():
    client, _ = _client_at("https://app.autolab.ai")
    info = await client.get_hill("ottogin", "erdos-3")
    # Keep only task-level public metadata, never account/session responses.
    public = {k: info[k] for k in (
        "name", "owner", "slug", "description", "visibility", "current_tree_hash", "versions"
    ) if k in info}
    save("hill-metadata.json", public)
    print("hill current_tree_hash:", public.get("current_tree_hash"))

    context_list = await client.get_list("alejandrozu", "openmath")
    public_list = {k: context_list[k] for k in (
        "name", "slug", "title", "description", "visibility"
    ) if k in context_list}
    public_list["source"] = "https://app.autolab.ai/lists/alejandrozu/openmath"
    public_list["body_md_excerpt"] = context_list.get("body_md", "").split("## Research catalog")[0]
    public_list["hills"] = {
        slug: row["hill"] for slug, row in context_list.get("hills", {}).items()
    }
    save("openmath-list.json", public_list)
    print("public list metadata saved")

    access = get_json("https://ghcr.io/token?scope=repository:ottogin/lean-mathlib:pull")
    headers = {
        "Authorization": "Bearer " + access["token"],
        "Accept": "application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json",
    }
    manifest = get_json("https://ghcr.io/v2/ottogin/lean-mathlib/manifests/" + IMAGE_DIGEST, headers)
    save("image-manifest.json", manifest)
    config = get_json("https://ghcr.io/v2/ottogin/lean-mathlib/blobs/" + manifest["config"]["digest"], headers)
    save("image-config.json", config)
    print("image architecture:", config.get("architecture"))
    print("image layers:", len(manifest.get("layers", [])))


if __name__ == "__main__":
    asyncio.run(main())
