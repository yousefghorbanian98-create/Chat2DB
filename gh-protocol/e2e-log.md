## gh-protocol E2E log — 2026-10-26T01:31:47Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-26T01:29:57Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 26 01:24 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 26 01:30 .
drwxr-xr-x 3 runner runner 4096 Oct 26 01:30 ..
drwxr-xr-x 3 runner runner 4096 Oct 26 01:30 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 26 01:30 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3333
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7ff649201000 as it is in the protected range from 0x7ff549200000 to 0x7ff649400000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Successfully initialized netsim WiFi
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 37240 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 126
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3333) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:32869 is gone due to Stream removed (CANCELLED)

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:mergeDebugNativeLibs
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:compileDebugKotlin
e: The daemon has terminated unexpectedly on startup attempt #1 with error code: 0. The daemon process output:
    1. Kotlin compile daemon is ready
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:608:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792978012885.json

BUILD SUCCESSFUL in 2m 44s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~8s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3256)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tunnel up after ~4s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
tapped VPN consent at: 894 1519 (iter vpn-1)
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::2/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::19a3:f060:6745:f880/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.116.4): 56(84) bytes.

--- 140.82.116.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
relay self-test PASS (real remote payload through the relay)
10-26 01:31:40.751  3256  4416 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:31:40.752  3256  4416 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=220 firstByteMs=430 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-26 01:31:33.916  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=499
10-26 01:31:33.917  3256  4572 D GhDiag  : dns_reply 511ms path=doh:cloudflare-dns.com bytes=260
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=206
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_reply 735ms path=doh:cloudflare-dns.com bytes=164
10-26 01:31:34.147  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:31:34.148  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:34.273  3256  4605 D GhDiag  : flow_established 101ms
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=218
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_reply 886ms path=doh:cloudflare-dns.com bytes=161
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=93
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_reply 979ms path=doh:cloudflare-dns.com bytes=61
10-26 01:31:34.477  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:34.579  3256  4620 D GhDiag  : flow_established 20ms
10-26 01:31:35.364  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:35.389  3256  4631 D GhDiag  : flow_established 2ms
10-26 01:31:36.311  3256  4414 D GhDiag  : stats t=5s packets=50 tcp=30 dns53=4 otherUdp=6 activeTcp=3 flowsOpened=7 flowsEstablished=7 connectFailures=0 retransmits=0 appUp=1934 appDown=4622 probeUp=91 probeDown=402 probeFlows=1 dnsOk=4 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:31:36.715  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:36.721  3256  4679 D GhDiag  : flow_established 5ms
10-26 01:31:36.822  3256  4417 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5510 probe=true
10-26 01:31:37.068  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=80
10-26 01:31:37.265  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=182
10-26 01:31:37.277  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.450  3256  4708 D GhDiag  : flow_established 22ms
10-26 01:31:37.720  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.765  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:37.789  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=520
10-26 01:31:37.804  3256  4726 D GhDiag  : flow_established 14ms
10-26 01:31:37.883  3256  4724 D GhDiag  : flow_established 58ms
10-26 01:31:37.891  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=84
10-26 01:31:37.913  3256  4415 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-26 01:31:38.015  3256  4735 D GhDiag  : flow_established 5ms
10-26 01:31:38.329  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=409
10-26 01:31:38.599  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=265
10-26 01:31:38.761  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:38.830  3256  4745 D GhDiag  : flow_established 4ms
10-26 01:31:39.369  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:39.574  3256  4756 D GhDiag  : flow_established 60ms
10-26 01:31:39.847  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=260
10-26 01:31:40.123  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=256
10-26 01:31:40.147  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.198  3256  4766 D GhDiag  : flow_established 40ms
10-26 01:31:40.475  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42814->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6328 probe=false
10-26 01:31:40.751  3256  4416 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:31:40.752  3256  4416 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=220 firstByteMs=430 checksums=0
10-26 01:31:40.808  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.843  3256  4782 D GhDiag  : flow_established 4ms
10-26 01:31:41.283  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:41.314  3256  4790 D GhDiag  : flow_established 2ms
10-26 01:31:41.328  3256  4414 D GhDiag  : stats t=10s packets=646 tcp=609 dns53=12 otherUdp=10 activeTcp=12 flowsOpened=17 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=51106 appDown=1272910 probeUp=91 probeDown=402 probeFlows=0 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:31:41.628  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42828->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6265 probe=false
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=51106 bytes
10-26 01:31:41.328  3256  4414 D GhDiag  : stats t=10s packets=646 tcp=609 dns53=12 otherUdp=10 activeTcp=12 flowsOpened=17 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=51106 appDown=1272910 probeUp=91 probeDown=402 probeFlows=0 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-26 01:31:40.751  3256  4416 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-26 01:31:24.534  3256  3256 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:31:24.534  3256  3256 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:31:24.919  3256  3256 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:31:25.012  3256  3256 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:31:25.012  3256  3256 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:31:25.012  3256  3256 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:31:25.152  3256  3256 D GhDiag  : connect: core.start=true 
10-26 01:31:31.305  3256  3256 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.313  3256  4416 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:31:31.526  3256  4418 D GhDiag  : flow_established 8ms
10-26 01:31:31.746  3256  4416 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:31:31.757  3256  4459 D GhDiag  : flow_established 10ms
10-26 01:31:32.206  3256  4415 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:31:32.213  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:60994->fd00:1:…:853
10-26 01:31:32.214  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:60994->fd00:1::1:853
10-26 01:31:32.273  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=63
10-26 01:31:32.294  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=144
10-26 01:31:32.294  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=1274
10-26 01:31:32.295  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:31:32.295  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:32.338  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:31:32.338  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:32.374  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.418  3256  4511 D GhDiag  : flow_established 26ms
10-26 01:31:32.428  3256  4510 D GhDiag  : flow_established 54ms
10-26 01:31:32.490  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:31:32.491  3256  4415 D GhDiag  : flow_closed dst=fd00:1:…:42722->2001:4860:…:443 reason=client_rst up=0 down=0 ms=153 probe=false
10-26 01:31:32.494  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.495  3256  4415 D GhDiag  : flow_closed dst=10.8.x.x:38410->142.251.x.x:443 reason=client_rst up=0 down=0 ms=200 probe=false
10-26 01:31:32.582  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.618  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:31:32.785  3256  4462 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:31:32.789  3256  4462 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1043 probe=false
10-26 01:31:32.807  3256  4415 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:31:32.848  3256  4415 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:31:32.849  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:46600->10.8.x.x:853
10-26 01:31:32.849  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:46600->10.8.0.1:853
10-26 01:31:33.010  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:33.048  3256  4415 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:31:33.050  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:32774->fd00:1:…:853
10-26 01:31:33.052  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:32774->fd00:1::1:853
10-26 01:31:33.056  3256  4415 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:31:33.056  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:39596->10.8.x.x:853
10-26 01:31:33.056  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:39596->10.8.0.1:853
10-26 01:31:33.269  3256  4415 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=94
10-26 01:31:33.273  3256  4415 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=891
10-26 01:31:33.406  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:31:33.407  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:31:33.474  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:31:33.475  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:31:33.871  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:33.916  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=499
10-26 01:31:33.917  3256  4572 D GhDiag  : dns_reply 511ms path=doh:cloudflare-dns.com bytes=260
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=206
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_reply 735ms path=doh:cloudflare-dns.com bytes=164
10-26 01:31:34.147  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:31:34.148  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:34.273  3256  4605 D GhDiag  : flow_established 101ms
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=218
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_reply 886ms path=doh:cloudflare-dns.com bytes=161
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=93
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_reply 979ms path=doh:cloudflare-dns.com bytes=61
10-26 01:31:34.477  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:34.579  3256  4620 D GhDiag  : flow_established 20ms
10-26 01:31:35.364  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:35.389  3256  4631 D GhDiag  : flow_established 2ms
10-26 01:31:36.311  3256  4414 D GhDiag  : stats t=5s packets=50 tcp=30 dns53=4 otherUdp=6 activeTcp=3 flowsOpened=7 flowsEstablished=7 connectFailures=0 retransmits=0 appUp=1934 appDown=4622 probeUp=91 probeDown=402 probeFlows=1 dnsOk=4 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:31:36.715  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:36.721  3256  4679 D GhDiag  : flow_established 5ms
10-26 01:31:36.822  3256  4417 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5510 probe=true
10-26 01:31:37.068  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=80
10-26 01:31:37.265  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=182
10-26 01:31:37.277  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.450  3256  4708 D GhDiag  : flow_established 22ms
10-26 01:31:37.720  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.765  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:37.789  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=520
10-26 01:31:37.804  3256  4726 D GhDiag  : flow_established 14ms
10-26 01:31:37.883  3256  4724 D GhDiag  : flow_established 58ms
10-26 01:31:37.891  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=84
10-26 01:31:37.913  3256  4415 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-26 01:31:38.015  3256  4735 D GhDiag  : flow_established 5ms
10-26 01:31:38.329  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=409
10-26 01:31:38.599  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=265
10-26 01:31:38.761  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:38.830  3256  4745 D GhDiag  : flow_established 4ms
10-26 01:31:39.369  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:39.574  3256  4756 D GhDiag  : flow_established 60ms
10-26 01:31:39.847  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=260
10-26 01:31:40.123  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=256
10-26 01:31:40.147  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.198  3256  4766 D GhDiag  : flow_established 40ms
10-26 01:31:40.475  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42814->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6328 probe=false
10-26 01:31:40.751  3256  4416 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:31:40.752  3256  4416 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=220 firstByteMs=430 checksums=0
10-26 01:31:40.808  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.843  3256  4782 D GhDiag  : flow_established 4ms
10-26 01:31:41.283  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:41.314  3256  4790 D GhDiag  : flow_established 2ms
10-26 01:31:41.328  3256  4414 D GhDiag  : stats t=10s packets=646 tcp=609 dns53=12 otherUdp=10 activeTcp=12 flowsOpened=17 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=51106 appDown=1272910 probeUp=91 probeDown=402 probeFlows=0 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:31:41.628  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42828->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6265 probe=false
10-26 01:31:42.387  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:42.649  3256  4816 D GhDiag  : flow_established 77ms
10-26 01:31:42.900  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42830->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6188 probe=false
10-26 01:31:43.336  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=358
10-26 01:31:43.464  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=127
10-26 01:31:43.835  3256  4415 D GhDiag  : flow_open v4 dst=173.194.x.x:5228 probe=false
10-26 01:31:43.857  3256  4840 D GhDiag  : flow_established 3ms
10-26 01:31:44.030  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42832->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6262 probe=false
10-26 01:31:44.924  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=387
10-26 01:31:45.066  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=129
10-26 01:31:45.160  3256  4415 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:31:45.212  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=131
10-26 01:31:45.268  3256  4879 D GhDiag  : flow_established 48ms
10-26 01:31:45.357  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=145
10-26 01:31:45.442  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:45.446  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:45.452  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=73
10-26 01:31:45.493  3256  4896 D GhDiag  : flow_established 39ms
10-26 01:31:45.594  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=141
10-26 01:31:45.622  3256  4897 D GhDiag  : flow_established 7ms
10-26 01:31:45.724  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:45.790  3256  4909 D GhDiag  : flow_established 3ms
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
6 01:31:18.100   520   533 D CoreBackPreview: Window{42da61c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@66c2efe, mPriority=0, mIsAnimationCallback=false}
10-26 01:31:18.895  1047  1047 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-26 01:31:18.909  1047  1349 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-26 01:31:19.426   520   537 W ziparchive: Unable to open '/data/app/~~3GqDBmayXZxnFh1NHD9JxQ==/com.ghprotocol.app-dChyvJn3kED6Rj5XlnnUQw==/base.dm': No such file or directory
10-26 01:31:19.427   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s910ms
10-26 01:31:19.471   520  2238 W InputManager-JNI: Input channel object '371d10a Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-26 01:31:19.472   520   990 D CoreBackPreview: Window{371d10a u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-26 01:31:21.424   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{12a943d com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:31:21.425   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{4199583 com.android.camera2/10147} BLOCKED
10-26 01:31:21.425   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{c4c300 com.google.android.gm/10140} BLOCKED
10-26 01:31:21.425   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{9313739 com.google.android.dialer/10128} BLOCKED
10-26 01:31:21.426   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{7de117e com.google.android.contacts/10153} BLOCKED
10-26 01:31:21.426   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{85606df com.google.android.apps.youtube.music/10156} BLOCKED
10-26 01:31:21.681   520   616 I InputDispatcher: 42da61c com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2238ms processing FocusEvent(hasFocus=true)
10-26 01:31:21.752   520  2705 I ImeTracker: com.ghprotocol.app:1f3b295c: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:31:21.752   520  2705 I ImeTracker: com.ghprotocol.app:1f3b295c: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:31:21.814  1509  1509 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:31:22.621   520   950 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{bc75fb6 com.google.android.gm/10140} BLOCKED
10-26 01:31:22.959  3256  3824 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-26 01:31:24.132   520  2177 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-26 01:31:24.136   828   864 V WindowManagerShell: Transition requested: android.os.BinderProxy@11a1ab7 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=56148 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@ccb5224} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{171218d com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:31:24.287  3922  3922 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:31:24.292  3922  3922 I AndroidRuntime: Using default boot image
10-26 01:31:24.292  3922  3922 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:31:24.424  3922  3922 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:31:24.534  3256  3256 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:31:24.534  3256  3256 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:31:24.762  3961  3961 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:31:24.762  3961  3961 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:31:24.919  3256  3256 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:31:25.012  3256  3256 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:31:25.012  3256  3256 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:31:25.012  3256  3256 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:31:25.152  3256  3256 D GhDiag  : connect: core.start=true 
10-26 01:31:25.363  1447  3662 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-26 01:31:25.593   520   588 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{fc0a634 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:31:25.911   520  1681 D CoreBackPreview: Window{ffb9e3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@5b4227b, mPriority=0, mIsAnimationCallback=false}
10-26 01:31:25.912  1399  3425 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-26 01:31:26.107  3922  3922 D AndroidRuntime: Shutting down VM
10-26 01:31:26.142  4023  4023 W libxraycore.so: type=1400 audit(0.0:32): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=55409 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-26 01:31:26.347  3256  3265 I .ghprotocol.app: Background concurrent copying GC freed 105509(5479KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6454KB/12MB, paused 48.288ms,7us total 537.055ms
10-26 01:31:27.404  4191  4191 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:31:27.428  4191  4191 I AndroidRuntime: Using default boot image
10-26 01:31:27.428  4191  4191 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:31:27.563  4191  4191 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:31:28.065   520  1865 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-26 01:31:28.066   520  1865 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-26 01:31:28.066   520  1865 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-26 01:31:28.854   520   537 V WindowManager: Sent Transition #7 createdAt=10-26 01:31:24.084 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=56148 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{e4d1361 Task{5cf6a20 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{cf27d90 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:31:28.855   828   864 V WindowManagerShell: onTransitionReady android.os.BinderProxy@11a1ab7: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=TRANSLUCENT|FILLS_TASK leash=Surface(name=ActivityRecord{39bd987 u0 com.android.vpndialogs/.ConfirmDialog)/@0xc4e4cd1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{13a13b9 u0 com.ghprotocol.app/.MainActivity)/@0x3649336 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{81596b4 u0 com.ghprotocol.app/.MainActivity)/@0x8715237 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:31:28.855   828   864 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=TRANSLUCENT|FILLS_TASK leash=Surface(name=ActivityRecord{39bd987 u0 com.android.vpndialogs/.ConfirmDialog)/@0xc4e4cd1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{13a13b9 u0 com.ghprotocol.app/.MainActivity)/@0x3649336 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{81596b4 u0 com.ghprotocol.app/.MainActivity)/@0x8715237 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:31:28.856   828   864 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=TRANSLUCENT|FILLS_TASK leash=Surface(name=ActivityRecord{39bd987 u0 com.android.vpndialogs/.ConfirmDialog)/@0xc4e4cd1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{13a13b9 u0 com.ghprotocol.app/.MainActivity)/@0x3649336 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{81596b4 u0 com.ghprotocol.app/.MainActivity)/@0x8715237 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:31:28.856   520   537 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=TRANSLUCENT|FILLS_TASK leash=Surface(name=ActivityRecord{39bd987 u0 com.android.vpndialogs/.ConfirmDialog)/@0x192d842 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{13a13b9 u0 com.ghprotocol.app/.MainActivity)/@0xb9d8e8d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{81596b4 u0 com.ghprotocol.app/.MainActivity)/@0xd615324 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:31:29.210  4191  4191 D AndroidRuntime: Shutting down VM
10-26 01:31:29.452  1588  1588 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-26 01:31:29.453  1588  2241 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-26 01:31:29.453  1588  2241 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-26 01:31:30.722   520  1392 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-26 01:31:31.167   520   816 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-26 01:31:31.304   520   816 I Vpn     : Established by com.ghprotocol.app on tun0
10-26 01:31:31.305  3256  3256 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:31:31.310  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.311  3256  4415 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:31:31.313  3256  4416 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:31:31.428   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{3c8e254 com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:31:31.428   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{27625fd com.google.android.gm/10140} BLOCKED
10-26 01:31:31.428   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{a8f72f2 com.google.android.devicelockcontroller/10189} BLOCKED
10-26 01:31:31.429   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{d45dd43 com.google.android.rkpdapp/10173} BLOCKED
10-26 01:31:31.429   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{4fbcfc0 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:31:31.429   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{b68f357 com.google.android.projection.gearhead/10123} BLOCKED
10-26 01:31:31.526  3256  4418 D GhDiag  : flow_established 8ms
10-26 01:31:31.746  3256  4416 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:31:31.757  3256  4459 D GhDiag  : flow_established 10ms
10-26 01:31:31.895   520  2212 I ImeTracker: com.ghprotocol.app:636203c6: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:31:31.896   520  2212 I ImeTracker: com.ghprotocol.app:636203c6: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:31:31.901  1509  1509 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:31:32.206  3256  4415 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:31:32.213  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:60994->fd00:1:…:853
10-26 01:31:32.214  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:60994->fd00:1::1:853
10-26 01:31:32.273  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=63
10-26 01:31:32.294  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=144
10-26 01:31:32.294  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=1274
10-26 01:31:32.295  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:31:32.295  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:32.338  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:31:32.338  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:32.374  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.418  3256  4511 D GhDiag  : flow_established 26ms
10-26 01:31:32.428  3256  4510 D GhDiag  : flow_established 54ms
10-26 01:31:32.490  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:31:32.491  3256  4415 D GhDiag  : flow_closed dst=fd00:1:…:42722->2001:4860:…:443 reason=client_rst up=0 down=0 ms=153 probe=false
10-26 01:31:32.494  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.495  3256  4415 D GhDiag  : flow_closed dst=10.8.x.x:38410->142.251.x.x:443 reason=client_rst up=0 down=0 ms=200 probe=false
10-26 01:31:32.582  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:32.618  3256  4415 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:31:32.785  3256  4462 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:31:32.789  3256  4462 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1043 probe=false
10-26 01:31:32.807  3256  4415 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:31:32.848  3256  4415 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:31:32.849  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:46600->10.8.x.x:853
10-26 01:31:32.849  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:46600->10.8.0.1:853
10-26 01:31:32.852  3256  3264 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-26 01:31:33.010  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:33.048  3256  4415 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:31:33.050  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:32774->fd00:1:…:853
10-26 01:31:33.052  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:32774->fd00:1::1:853
10-26 01:31:33.056  3256  4415 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:31:33.056  3256  4415 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:39596->10.8.x.x:853
10-26 01:31:33.056  3256  4415 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:39596->10.8.0.1:853
10-26 01:31:33.269  3256  4415 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=94
10-26 01:31:33.273  3256  4415 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=891
10-26 01:31:33.406  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:31:33.407  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:31:33.474  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:31:33.475  3256  4415 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:31:33.871  3256  4415 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:31:33.916  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=499
10-26 01:31:33.917  3256  4572 D GhDiag  : dns_reply 511ms path=doh:cloudflare-dns.com bytes=260
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=206
10-26 01:31:34.142  3256  4572 D GhDiag  : dns_reply 735ms path=doh:cloudflare-dns.com bytes=164
10-26 01:31:34.147  3256  4415 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:31:34.148  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:34.273  3256  4605 D GhDiag  : flow_established 101ms
10-26 01:31:34.298  3256  3265 I .ghprotocol.app: Background young concurrent copying GC freed 66247(5348KB) AllocSpace objects, 0(0B) LOS objects, 39% free, 7865KB/12MB, paused 1.501ms,12us total 104.370ms
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=218
10-26 01:31:34.360  3256  4572 D GhDiag  : dns_reply 886ms path=doh:cloudflare-dns.com bytes=161
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=93
10-26 01:31:34.454  3256  4572 D GhDiag  : dns_reply 979ms path=doh:cloudflare-dns.com bytes=61
10-26 01:31:34.477  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:34.579  3256  4620 D GhDiag  : flow_established 20ms
10-26 01:31:35.364  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:35.389  3256  4631 D GhDiag  : flow_established 2ms
10-26 01:31:36.311  3256  4414 D GhDiag  : stats t=5s packets=50 tcp=30 dns53=4 otherUdp=6 activeTcp=3 flowsOpened=7 flowsEstablished=7 connectFailures=0 retransmits=0 appUp=1934 appDown=4622 probeUp=91 probeDown=402 probeFlows=1 dnsOk=4 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:31:36.556   520  2695 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4671, uid=2000 that is not exported from uid 10192
10-26 01:31:36.715  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:36.721  3256  4679 D GhDiag  : flow_established 5ms
10-26 01:31:36.822  3256  4417 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5510 probe=true
10-26 01:31:36.922  3256  3265 I .ghprotocol.app: Background young concurrent copying GC freed 55581(4814KB) AllocSpace objects, 0(0B) LOS objects, 38% free, 7984KB/12MB, paused 11us,13us total 135.181ms
10-26 01:31:37.068  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=80
10-26 01:31:37.265  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=182
10-26 01:31:37.277  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.450  3256  4708 D GhDiag  : flow_established 22ms
10-26 01:31:37.720  3256  4415 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:31:37.765  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:37.789  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=520
10-26 01:31:37.804  3256  4726 D GhDiag  : flow_established 14ms
10-26 01:31:37.883  3256  4724 D GhDiag  : flow_established 58ms
10-26 01:31:37.891  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=84
10-26 01:31:37.913  3256  4415 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-26 01:31:38.015  3256  4735 D GhDiag  : flow_established 5ms
10-26 01:31:38.329  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=409
10-26 01:31:38.599  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=265
10-26 01:31:38.761  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:38.822  3256  3265 I .ghprotocol.app: Background young concurrent copying GC freed 57815(4650KB) AllocSpace objects, 0(0B) LOS objects, 16% free, 10MB/12MB, paused 6.631ms,40us total 738.725ms
10-26 01:31:38.830  3256  4745 D GhDiag  : flow_established 4ms
10-26 01:31:39.369  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:39.574  3256  4756 D GhDiag  : flow_established 60ms
10-26 01:31:39.847  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=260
10-26 01:31:40.123  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=256
10-26 01:31:40.147  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.198  3256  4766 D GhDiag  : flow_established 40ms
10-26 01:31:40.475  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42814->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6328 probe=false
10-26 01:31:40.751  3256  4416 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:31:40.752  3256  4416 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=220 firstByteMs=430 checksums=0
10-26 01:31:40.808  3256  4415 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:31:40.843  3256  4782 D GhDiag  : flow_established 4ms
10-26 01:31:41.008  3256  4415 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-37776 (4739) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:458) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.onPacket(byte[]) for 189ms
10-26 01:31:41.074  3256  3265 I .ghprotocol.app: Background young concurrent copying GC freed 82961(7307KB) AllocSpace objects, 0(0B) LOS objects, 41% free, 8800KB/14MB, paused 23.580ms,2.562ms total 549.924ms
10-26 01:31:41.283  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:41.314  3256  4790 D GhDiag  : flow_established 2ms
10-26 01:31:41.328  3256  4414 D GhDiag  : stats t=10s packets=646 tcp=609 dns53=12 otherUdp=10 activeTcp=12 flowsOpened=17 flowsEstablished=16 connectFailures=0 retransmits=0 appUp=51106 appDown=1272910 probeUp=91 probeDown=402 probeFlows=0 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:31:41.628  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42828->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6265 probe=false
10-26 01:31:41.921   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{cfb5414 com.google.android.apps.messaging/10130} BLOCKED
10-26 01:31:41.921   520   570 I AppsFilter: interaction: PackageSetting{e6d2194 com.ghprotocol.app/10192} -> PackageSetting{61914bd com.google.android.contacts/10153} BLOCKED
10-26 01:31:42.387  3256  4415 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:31:42.649  3256  4816 D GhDiag  : flow_established 77ms
10-26 01:31:42.900  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42830->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6188 probe=false
10-26 01:31:43.320   520   537 V WindowManager:     info={id=9 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{99699d2 Task{7cb0968 #9 type=standard A=10149:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0xc54830f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{e4d1361 Task{5cf6a20 #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0xba7b6b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:31:43.336  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=358
10-26 01:31:43.464  3256  4572 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=127
10-26 01:31:43.470  3256  4415 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-37776 (4739) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:458) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.onPacket(byte[]) for 411ms
10-26 01:31:43.813  3256  3265 W .ghprotocol.app: Suspending all threads took: 7.124ms
10-26 01:31:43.826  3256  3265 I .ghprotocol.app: Background concurrent copying GC freed 80913(7090KB) AllocSpace objects, 33(660KB) LOS objects, 49% free, 8703KB/16MB, paused 17.008ms,7.265ms total 1.143s
10-26 01:31:43.835  3256  4415 D GhDiag  : flow_open v4 dst=173.194.x.x:5228 probe=false
10-26 01:31:43.857  3256  4840 D GhDiag  : flow_established 3ms
10-26 01:31:44.030  3256  4417 D GhDiag  : flow_closed dst=fd00:1:…:42832->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6262 probe=false

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
