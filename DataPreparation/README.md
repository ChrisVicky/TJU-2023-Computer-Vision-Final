# Data Preparation

* To collect enough data for the training process of Control Net, we have initially two options. First is to download videos and extract continuous frames including the movements of gestures. Second is to download massive GIFs from [Giphy](https://giphy.com/) and frames are extracted accordingly.
* Implementations on both choices are finished on time and archived here. 
* Essentially, because we require large diversity in datasets therefore we take only 2 frames every 2 minutes in a video which ends up wasting streams, we take GIFs as the final decision.
* Yet, still we keep the Video manipulation methods Archived here for future use.

## File Structures

```
.
├── coca_annotator.py          : [GIFs] - [CLIP] - prompt generator
├── get_random.py              : [GIFs] - [APIs] - Random
├── get_trending.py            : [GIFs] - [APIs] - Trending
├── img2flow.py                : [GIFs] - [RAFT] - Optical Flow Extractor for images
├── gif2figure.py              : [GIFs] - GIF to Image
├── gif_downloader.py          : [GIFs] - Multi-Threads-GIF-Downloader
├── integrity_verification.py  : [GIFs] - Dataset Validator
├── proxy_pool.py              : [GIFs] - Proxy Issues
├── redis2file.py              : [GIFs] - Store Redis to Json
├── Redis.py                   : [GIFs] - Redis Usage
├── README.md
├── lux                        : [Videos] - [downloader](https://github.com/ChrisVicky/lux)
├── op_flow_generator.py       : [Videos] - [RAFT] Optical Flow Extractors
├── main.py                    : [Videos] - Video Control
├── video2gif.py               : [Videos] - Transform Videos to GIFs
└── video_downloader.py        : [Videos] - Videos Downloading Control

3 directories, 24 files
```

## Videos Manipulation

* [lux](https://github.com/ChrisVicky/lux) is a video downloader for multiple platforms.

### Usage
1. Copy your cookies in file `cookies` stored in the current directory
2. RUN `python download.py` to start downloading

## GIFs Manipulation

1. Download massive GIFs from [`Giphy`](https://giphy.com/).
2. Since `giphy` provides APIs for querying trending GIFs and other stuff at its [Developer Page](https://developers.giphy.com/), it is better to collect GIFs via APIs rather than Crawling its home page.
3. The return items of the APIs contain `Image Item` providing the URL of the GIF. Therefore, we decide to develop the system in the following way:

```markdown
┌──────────────────┐ ┌──────────────────────┐ ┌─────────────────┐   Check IMG sizes
│  URL COLLECTORS  │┌►     DOWNLOADERS      │┌►    (FIGUREs)    │ ◄────────────────┐
│┌──────┐┌────────┐│││┌────────────────────┐││└─┬─────────────┬─┘                  │
││Random││Trending│││││[concurrent.futures]│││  │   [RAFT]    │                    │┌─────────────┐
│└─┬────┘└──────┬─┘│││└─┬─┬─┬──────────────┘││┌─│─────────────│─┐   Check .flo     ││             │
│  │  [APIs]    │  │││  │ │ │ ... n threads │││ ▼(.jpg + .flo)▼ │ ◄────────────────┼┤  VALIDATOR  │
└──│────────────│──┘│└──│─│─│───────────────┘│└─┬─────────────┬─┘                  ││             │
┌──│────────────│──┐│   │ │ │       [GIF2FIG]│  │   [CLIP]    │                    │└─────────────┘
│  ▼   REDIS    ▼  ├┘┌──│─│─│───────────────┐│┌─▼─────────────▼─┐   Check Prompt   │
│    (hash:url)    │ │  ▼ ▼ ▼ (GIFs)        ├┘│ (.jpg+.flo+text)│ ◄────────────────┘
└──────────────────┘ └──────────────────────┘ └─────────┬───────┘   
                                                        ▼
                                    [(0.jpg, 1.jpg, flow.jpg, metadata.json), ...]

```
