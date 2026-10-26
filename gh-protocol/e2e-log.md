## gh-protocol E2E log — 2026-10-26T01:19:27Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-26T01:17:40Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 26 01:12 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 26 01:18 .
drwxr-xr-x 3 runner runner 4096 Oct 26 01:18 ..
drwxr-xr-x 3 runner runner 4096 Oct 26 01:18 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 26 01:18 gh_test.ini

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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15988 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15988 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3084
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
WARNING: cannnot unmap ptr 0x7f40d7201000 as it is in the protected range from 0x7f3fd7200000 to 0x7f40d7400000
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
INFO         | Boot completed in 38538 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 117
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3084) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:46033 is gone due to Stream removed (CANCELLED)

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
> Task :app:mergeDebugAssets
> Task :app:processDebugManifest
> Task :app:mergeDebugResources
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugManifestForPackage
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:compileDebugKotlin
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792977270310.json

BUILD SUCCESSFUL in 2m 51s
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
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3136)
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
    inet6 fe80::4dc0:93c3:1fdb:c5d6/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.3): 56(84) bytes.

--- 140.82.114.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
relay self-test PASS (real remote payload through the relay)
10-26 01:19:17.614  3136  4373 D GhDiag  : relay_selftest_v6 ok=false stage=build detail=cannot_build_syn
10-26 01:19:17.693  3136  4373 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=19 firstByteMs=445 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-26 01:19:18.373  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=57
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=1000
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_reply 1111ms path=doh:cloudflare-dns.com bytes=178
10-26 01:19:18.774  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:18.775  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:19.134  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:19.135  3136  4389 D GhDiag  : dns_reply 1676ms path=doh:cloudflare-dns.com bytes=274
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=212
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_reply 1130ms path=doh:cloudflare-dns.com bytes=260
10-26 01:19:19.504  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=148
10-26 01:19:19.505  3136  4389 D GhDiag  : dns_reply 1274ms path=doh:cloudflare-dns.com bytes=164
10-26 01:19:19.539  3136  4372 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:19:19.909  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:19.919  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_reply 1697ms path=doh:cloudflare-dns.com bytes=61
10-26 01:19:20.257  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:19:20.258  3136  4389 D GhDiag  : dns_reply 1885ms path=doh:cloudflare-dns.com bytes=85
10-26 01:19:20.322  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=60
10-26 01:19:20.327  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:20.381  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=40
10-26 01:19:20.385  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=569
10-26 01:19:20.386  3136  4480 D GhDiag  : flow_established 23ms
10-26 01:19:20.438  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=179
10-26 01:19:20.441  3136  4389 D GhDiag  : dns_reply 522ms path=doh:cloudflare-dns.com bytes=152
10-26 01:19:20.558  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=116
10-26 01:19:20.563  3136  4389 D GhDiag  : dns_reply 644ms path=doh:cloudflare-dns.com bytes=168
10-26 01:19:20.563  3136  4372 D GhDiag  : flow_open v4 dst=104.154.x.x:443 probe=false
10-26 01:19:20.614  3136  4484 D GhDiag  : flow_established 40ms
10-26 01:19:20.776  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=90
10-26 01:19:20.953  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:21.006  3136  4499 D GhDiag  : flow_established 17ms
10-26 01:19:21.091  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=312
10-26 01:19:21.111  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:21.147  3136  4502 D GhDiag  : flow_established 11ms
10-26 01:19:21.821  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=282
10-26 01:19:22.165  3136  4371 D GhDiag  : stats t=5s packets=62 tcp=38 dns53=14 otherUdp=1 activeTcp=4 flowsOpened=5 flowsEstablished=5 connectFailures=0 retransmits=0 appUp=2659 appDown=9271 probeUp=91 probeDown=402 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:19:22.198  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.217  3136  4520 D GhDiag  : flow_established 6ms
10-26 01:19:22.294  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=469
10-26 01:19:22.474  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:22.687  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.690  3136  4533 D GhDiag  : flow_established 16ms
10-26 01:19:22.736  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=430
10-26 01:19:22.845  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.868  3136  4540 D GhDiag  : flow_established 59ms
10-26 01:19:22.964  3136  4547 D GhDiag  : flow_established 2ms
10-26 01:19:23.048  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:19:23.243  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:23.244  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=2659 bytes
10-26 01:19:22.165  3136  4371 D GhDiag  : stats t=5s packets=62 tcp=38 dns53=14 otherUdp=1 activeTcp=4 flowsOpened=5 flowsEstablished=5 connectFailures=0 retransmits=0 appUp=2659 appDown=9271 probeUp=91 probeDown=402 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-26 01:19:17.614  3136  4373 D GhDiag  : relay_selftest_v6 ok=false stage=build detail=cannot_build_syn
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-26 01:19:08.940  3136  3136 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:19:08.944  3136  3136 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:19:09.365  3136  3136 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:19:09.488  3136  3136 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:19:09.490  3136  3136 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:19:09.490  3136  3136 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:19:09.652  3136  3136 D GhDiag  : connect: core.start=true 
10-26 01:19:17.159  3136  3136 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:19:17.166  3136  4373 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:19:17.176  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:19:17.176  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:19:17.177  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:17.178  3136  4375 D GhDiag  : flow_established 4ms
10-26 01:19:17.219  3136  4372 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:19:17.220  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:45436->fd00:1:…:853
10-26 01:19:17.225  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:45436->fd00:1::1:853
10-26 01:19:17.225  3136  4372 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:19:17.227  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:45656->10.8.x.x:853
10-26 01:19:17.229  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:45656->10.8.0.1:853
10-26 01:19:17.335  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.336  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.381  3136  4372 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:19:17.458  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-26 01:19:17.459  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-26 01:19:17.481  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.483  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.504  3136  4372 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:19:17.517  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:45438->fd00:1:…:853
10-26 01:19:17.517  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:45438->fd00:1::1:853
10-26 01:19:17.525  3136  4372 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:19:17.550  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:45664->10.8.x.x:853
10-26 01:19:17.551  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:45664->10.8.0.1:853
10-26 01:19:17.614  3136  4373 D GhDiag  : relay_selftest_v6 ok=false stage=build detail=cannot_build_syn
10-26 01:19:17.622  3136  4377 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=upstream_eof up=91 down=402 ms=456 probe=true
10-26 01:19:17.693  3136  4373 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=19 firstByteMs=445 checksums=0
10-26 01:19:17.695  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:17.924  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.925  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.925  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:18.224  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:19:18.231  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:19:18.373  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=57
10-26 01:19:18.373  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=57
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=1000
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_reply 1111ms path=doh:cloudflare-dns.com bytes=178
10-26 01:19:18.774  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:18.775  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:19.134  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:19.135  3136  4389 D GhDiag  : dns_reply 1676ms path=doh:cloudflare-dns.com bytes=274
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=212
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_reply 1130ms path=doh:cloudflare-dns.com bytes=260
10-26 01:19:19.504  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=148
10-26 01:19:19.505  3136  4389 D GhDiag  : dns_reply 1274ms path=doh:cloudflare-dns.com bytes=164
10-26 01:19:19.539  3136  4372 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:19:19.909  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:19.919  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_reply 1697ms path=doh:cloudflare-dns.com bytes=61
10-26 01:19:20.257  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:19:20.258  3136  4389 D GhDiag  : dns_reply 1885ms path=doh:cloudflare-dns.com bytes=85
10-26 01:19:20.322  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=60
10-26 01:19:20.327  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:20.381  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=40
10-26 01:19:20.385  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=569
10-26 01:19:20.386  3136  4480 D GhDiag  : flow_established 23ms
10-26 01:19:20.438  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=179
10-26 01:19:20.441  3136  4389 D GhDiag  : dns_reply 522ms path=doh:cloudflare-dns.com bytes=152
10-26 01:19:20.558  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=116
10-26 01:19:20.563  3136  4389 D GhDiag  : dns_reply 644ms path=doh:cloudflare-dns.com bytes=168
10-26 01:19:20.563  3136  4372 D GhDiag  : flow_open v4 dst=104.154.x.x:443 probe=false
10-26 01:19:20.614  3136  4484 D GhDiag  : flow_established 40ms
10-26 01:19:20.776  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=90
10-26 01:19:20.953  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:21.006  3136  4499 D GhDiag  : flow_established 17ms
10-26 01:19:21.091  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=312
10-26 01:19:21.111  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:21.147  3136  4502 D GhDiag  : flow_established 11ms
10-26 01:19:21.821  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=282
10-26 01:19:22.165  3136  4371 D GhDiag  : stats t=5s packets=62 tcp=38 dns53=14 otherUdp=1 activeTcp=4 flowsOpened=5 flowsEstablished=5 connectFailures=0 retransmits=0 appUp=2659 appDown=9271 probeUp=91 probeDown=402 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:19:22.198  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.217  3136  4520 D GhDiag  : flow_established 6ms
10-26 01:19:22.294  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=469
10-26 01:19:22.474  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:22.687  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.690  3136  4533 D GhDiag  : flow_established 16ms
10-26 01:19:22.736  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=430
10-26 01:19:22.845  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.868  3136  4540 D GhDiag  : flow_established 59ms
10-26 01:19:22.964  3136  4547 D GhDiag  : flow_established 2ms
10-26 01:19:23.048  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:19:23.243  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:23.244  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:23.282  3136  4559 D GhDiag  : flow_established 11ms
10-26 01:19:23.314  3136  4558 D GhDiag  : flow_established 2ms
10-26 01:19:23.764  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:23.852  3136  4573 D GhDiag  : flow_established 25ms
10-26 01:19:24.096  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:24.168  3136  4589 D GhDiag  : flow_established 65ms
10-26 01:19:24.182  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:24.200  3136  4593 D GhDiag  : flow_established 10ms
10-26 01:19:25.270  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:25.333  3136  4614 D GhDiag  : flow_established 52ms
10-26 01:19:25.749  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=286
10-26 01:19:26.421  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=672
10-26 01:19:26.599  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:26.638  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:26.656  3136  4647 D GhDiag  : flow_established 4ms
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
droid.window.IOnBackInvokedCallback$Stub$Proxy@8343ca0, mPriority=0, mIsAnimationCallback=false}
10-26 01:19:04.537   520   539 W ziparchive: Unable to open '/data/app/~~rSQXubtUQP7tsVAPc_BDTw==/com.ghprotocol.app-ftGqdUAoz2waXHnCUfUe9Q==/base.dm': No such file or directory
10-26 01:19:04.584   520  2426 D CoreBackPreview: Window{8b6f127 u0 Splash Screen com.ghprotocol.app}: Setting back callback null
10-26 01:19:04.585   520  2178 W InputManager-JNI: Input channel object '8b6f127 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-26 01:19:04.602   520   539 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +4s319ms
10-26 01:19:05.029   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{1d697dc com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:19:05.029   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{acbe0e5 com.android.camera2/10145} BLOCKED
10-26 01:19:05.030   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{d72b7ba com.google.android.as/10125} BLOCKED
10-26 01:19:05.030   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{1af166b com.google.android.gm/10144} BLOCKED
10-26 01:19:05.030   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{22355c8 com.google.android.dialer/10128} BLOCKED
10-26 01:19:05.030   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{ddea661 com.google.android.apps.youtube.music/10156} BLOCKED
10-26 01:19:06.557   520   620 I InputDispatcher: 7ee158c com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2012ms processing FocusEvent(hasFocus=true)
10-26 01:19:06.670   520  2178 I ImeTracker: com.ghprotocol.app:149fbb88: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:19:06.670   520  2178 I ImeTracker: com.ghprotocol.app:149fbb88: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:19:06.689  1532  1532 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:19:07.235   520   950 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{bd5087f com.google.android.gm/10144} BLOCKED
10-26 01:19:07.338  3136  3613 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-26 01:19:08.514   520  1840 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-26 01:19:08.515   829   873 V WindowManagerShell: Transition requested: android.os.BinderProxy@f73339d TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=56706 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@6350012} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{a82b3e3 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:19:08.755  3780  3780 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:19:08.766  3780  3780 I AndroidRuntime: Using default boot image
10-26 01:19:08.766  3780  3780 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:19:08.940  3136  3136 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:19:08.944  3136  3136 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:19:09.175  3827  3827 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:19:09.175  3827  3827 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:19:09.175  3827  3827 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:19:09.175  3827  3827 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:19:09.247  3780  3780 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:19:09.365  3136  3136 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:19:09.488  3136  3136 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:19:09.490  3136  3136 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:19:09.490  3136  3136 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:19:09.593   520  1840 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{139db4 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:19:09.652  3136  3136 D GhDiag  : connect: core.start=true 
10-26 01:19:09.972   520   818 D CoreBackPreview: Window{d3f1bde u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@ae66c66, mPriority=0, mIsAnimationCallback=false}
10-26 01:19:10.346  3780  3780 D AndroidRuntime: Shutting down VM
10-26 01:19:11.003  3890  3890 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=55753 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-26 01:19:11.381  3136  3158 I .ghprotocol.app: Background concurrent copying GC freed 97816(5161KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6419KB/12MB, paused 139.188ms,9us total 784.873ms
10-26 01:19:11.771   829   873 V WindowManagerShell: onTransitionReady android.os.BinderProxy@f73339d: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{e2cf000 u0 com.ghprotocol.app/.MainActivity)/@0xc76fb9b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{eea7c7c u0 com.ghprotocol.app/.MainActivity)/@0x4348b38 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:19:11.771   829   873 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{e2cf000 u0 com.ghprotocol.app/.MainActivity)/@0xc76fb9b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{eea7c7c u0 com.ghprotocol.app/.MainActivity)/@0x4348b38 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:19:11.772   829   873 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{e2cf000 u0 com.ghprotocol.app/.MainActivity)/@0xc76fb9b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{eea7c7c u0 com.ghprotocol.app/.MainActivity)/@0x4348b38 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:19:11.789   520   539 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s264ms
10-26 01:19:11.789   520   539 V WindowManager: Sent Transition #7 createdAt=10-26 01:19:08.505 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=56706 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{fb323a0 Task{f63bd5a #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7e7b633 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:19:11.790   520   539 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{e2cf000 u0 com.ghprotocol.app/.MainActivity)/@0xe2ab96d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{eea7c7c u0 com.ghprotocol.app/.MainActivity)/@0x14edd84 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:19:12.046   829   873 V WindowManagerShell: Transition requested: android.os.BinderProxy@a76cf05 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=60180 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@a87db5a} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{24a018b com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:19:12.338  4059  4059 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:19:12.353  4059  4059 I AndroidRuntime: Using default boot image
10-26 01:19:12.353  4059  4059 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:19:12.396   520  2421 I ImeTracker: com.ghprotocol.app:b31e8517: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:19:12.396   520  2421 I ImeTracker: com.ghprotocol.app:b31e8517: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:19:12.607  1532  1532 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:19:12.788  4059  4059 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:19:13.127   520  2427 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-26 01:19:13.150   520  2427 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-26 01:19:13.150   520  2427 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-26 01:19:13.973   520   539 V WindowManager: Sent Transition #8 createdAt=10-26 01:19:11.968 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=60180 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{fb323a0 Task{f63bd5a #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2914465 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:19:15.488  4059  4059 D AndroidRuntime: Shutting down VM
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{a651daa com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{7939d9b com.google.android.apps.messaging/10130} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{4c18538 com.google.android.gm/10144} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{e4cf911 com.google.android.devicelockcontroller/10172} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{ecf6a76 com.google.android.rkpdapp/10191} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{e047877 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:19:15.719   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{9af2268 com.google.android.projection.gearhead/10123} BLOCKED
10-26 01:19:16.679   520   591 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-26 01:19:17.094   520   950 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-26 01:19:17.157   520  2419 I Vpn     : Established by com.ghprotocol.app on tun0
10-26 01:19:17.159  3136  3136 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:19:17.166  3136  4373 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:19:17.176  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:19:17.176  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:19:17.177  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:17.178  3136  4375 D GhDiag  : flow_established 4ms
10-26 01:19:17.219  3136  4372 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:19:17.220  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:45436->fd00:1:…:853
10-26 01:19:17.225  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:45436->fd00:1::1:853
10-26 01:19:17.225  3136  4372 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:19:17.227  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:45656->10.8.x.x:853
10-26 01:19:17.229  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:45656->10.8.0.1:853
10-26 01:19:17.335  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.336  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.381  3136  4372 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:19:17.401   520  2416 I ImeTracker: com.ghprotocol.app:e966547e: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-26 01:19:17.401   520  2416 I ImeTracker: com.ghprotocol.app:e966547e: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:19:17.408  1532  1532 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:19:17.458  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-26 01:19:17.459  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-26 01:19:17.481  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.483  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.504  3136  4372 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:19:17.517  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:45438->fd00:1:…:853
10-26 01:19:17.517  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:45438->fd00:1::1:853
10-26 01:19:17.525  3136  4372 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:19:17.550  3136  4372 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:45664->10.8.x.x:853
10-26 01:19:17.551  3136  4372 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:45664->10.8.0.1:853
10-26 01:19:17.614  3136  4373 D GhDiag  : relay_selftest_v6 ok=false stage=build detail=cannot_build_syn
10-26 01:19:17.622  3136  4377 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=upstream_eof up=91 down=402 ms=456 probe=true
10-26 01:19:17.693  3136  4373 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=19 firstByteMs=445 checksums=0
10-26 01:19:17.695  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:17.924  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.925  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:17.925  3136  4372 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:19:18.224  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:19:18.231  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:19:18.373  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=57
10-26 01:19:18.373  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=57
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=1000
10-26 01:19:18.569  3136  4389 D GhDiag  : dns_reply 1111ms path=doh:cloudflare-dns.com bytes=178
10-26 01:19:18.774  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:18.775  3136  4372 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:19:18.843  3136  3157 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-26 01:19:18.865  3136  3158 I .ghprotocol.app: Background young concurrent copying GC freed 91138(4947KB) AllocSpace objects, 2(40KB) LOS objects, 36% free, 8138KB/12MB, paused 67us,8us total 107.510ms
10-26 01:19:19.134  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:19.135  3136  4389 D GhDiag  : dns_reply 1676ms path=doh:cloudflare-dns.com bytes=274
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=212
10-26 01:19:19.354  3136  4389 D GhDiag  : dns_reply 1130ms path=doh:cloudflare-dns.com bytes=260
10-26 01:19:19.504  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=148
10-26 01:19:19.505  3136  4389 D GhDiag  : dns_reply 1274ms path=doh:cloudflare-dns.com bytes=164
10-26 01:19:19.539  3136  4372 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:19:19.905  1443  4441 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-26 01:19:19.909  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:19.919  3136  4372 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-26 01:19:19.951  1392  3663 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=555
10-26 01:19:20.070  3136  4389 D GhDiag  : dns_reply 1697ms path=doh:cloudflare-dns.com bytes=61
10-26 01:19:20.257  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:19:20.258  3136  4389 D GhDiag  : dns_reply 1885ms path=doh:cloudflare-dns.com bytes=85
10-26 01:19:20.322  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=60
10-26 01:19:20.327  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:20.381  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=40
10-26 01:19:20.385  3136  4372 D GhDiag  : tun v4 proto=6 dst=74.125.x.x:443 len=569
10-26 01:19:20.386  3136  4480 D GhDiag  : flow_established 23ms
10-26 01:19:20.438  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=179
10-26 01:19:20.441  3136  4389 D GhDiag  : dns_reply 522ms path=doh:cloudflare-dns.com bytes=152
10-26 01:19:20.558  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=116
10-26 01:19:20.563  3136  4389 D GhDiag  : dns_reply 644ms path=doh:cloudflare-dns.com bytes=168
10-26 01:19:20.563  3136  4372 D GhDiag  : flow_open v4 dst=104.154.x.x:443 probe=false
10-26 01:19:20.614  3136  4484 D GhDiag  : flow_established 40ms
10-26 01:19:20.776  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=90
10-26 01:19:20.953  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:21.006  3136  4499 D GhDiag  : flow_established 17ms
10-26 01:19:21.083  3136  3158 W .ghprotocol.app: Suspending all threads took: 5.016ms
10-26 01:19:21.091  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=312
10-26 01:19:21.097  3136  3158 I .ghprotocol.app: Background young concurrent copying GC freed 52197(4282KB) AllocSpace objects, 0(0B) LOS objects, 32% free, 8680KB/12MB, paused 32us,5.129ms total 194.494ms
10-26 01:19:21.111  3136  4372 D GhDiag  : flow_open v4 dst=74.125.x.x:443 probe=false
10-26 01:19:21.147  3136  4502 D GhDiag  : flow_established 11ms
10-26 01:19:21.821  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=282
10-26 01:19:22.165  3136  4371 D GhDiag  : stats t=5s packets=62 tcp=38 dns53=14 otherUdp=1 activeTcp=4 flowsOpened=5 flowsEstablished=5 connectFailures=0 retransmits=0 appUp=2659 appDown=9271 probeUp=91 probeDown=402 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:19:22.198  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.217  3136  4520 D GhDiag  : flow_established 6ms
10-26 01:19:22.294  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=469
10-26 01:19:22.474  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:22.687  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.690  3136  4533 D GhDiag  : flow_established 16ms
10-26 01:19:22.736  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=430
10-26 01:19:22.845  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:22.868  3136  4540 D GhDiag  : flow_established 59ms
10-26 01:19:22.964  3136  4547 D GhDiag  : flow_established 2ms
10-26 01:19:23.048  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:19:23.243  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:23.244  3136  4372 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:19:23.282  3136  4559 D GhDiag  : flow_established 11ms
10-26 01:19:23.314  3136  4558 D GhDiag  : flow_established 2ms
10-26 01:19:23.764  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:23.852  3136  4573 D GhDiag  : flow_established 25ms
10-26 01:19:24.096  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:24.168  3136  4589 D GhDiag  : flow_established 65ms
10-26 01:19:24.182  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:24.200  3136  4593 D GhDiag  : flow_established 10ms
10-26 01:19:24.658  3136  3158 W .ghprotocol.app: Suspending all threads took: 10.577ms
10-26 01:19:24.659  3136  3158 I .ghprotocol.app: Background young concurrent copying GC freed 49940(3799KB) AllocSpace objects, 0(0B) LOS objects, 29% free, 8998KB/12MB, paused 65.377ms,10.650ms total 415.371ms
10-26 01:19:24.964   520   539 V WindowManager:     info={id=10 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{579d17e Task{767a238 #9 type=standard A=10150:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0x3d9a432 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{fb323a0 Task{f63bd5a #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0x646ebd2 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:19:25.270  3136  4372 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:19:25.333  3136  4614 D GhDiag  : flow_established 52ms
10-26 01:19:25.749  3136  4389 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=286
10-26 01:19:25.945   520   573 I AppsFilter: interaction: PackageSetting{984844f com.ghprotocol.app/10192} -> PackageSetting{e6618b0 com.google.android.apps.messaging/10130} BLOCKED

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
