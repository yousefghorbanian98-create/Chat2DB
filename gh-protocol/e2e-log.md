## gh-protocol E2E log — 2026-10-25T23:14:52Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T23:12:50Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 23:08 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 23:13 .
drwxr-xr-x 3 runner runner 4096 Oct 25 23:13 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 23:13 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 23:13 gh_test.ini

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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15993 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15993 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3124
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
WARNING: cannnot unmap ptr 0x7fde16001000 as it is in the protected range from 0x7fdd16000000 to 0x7fde16200000
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
INFO         | Boot completed in 37504 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 119
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3124) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:39515 is gone due to Stream removed (CANCELLED)

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
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:compressDebugAssets

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792969814878.json

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
emulator can reach raw.githubusercontent.com after ~12s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3314)
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
    inet6 fe80::eafa:4853:1eca:8ecd/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.4): 56(84) bytes.

--- 140.82.113.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
relay self-test PASS (real remote payload through the relay)
10-25 23:14:42.186  3314  4303 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=29 firstByteMs=84 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-25 23:14:43.445  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-25 23:14:43.445  3314  4302 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:14:43.489  3314  4450 D GhDiag  : flow_established 2ms
10-25 23:14:43.490  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=40
10-25 23:14:43.491  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=270
10-25 23:14:43.539  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.682  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.683  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.789  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=560
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_reply 579ms path=doh:cloudflare-dns.com bytes=178
10-25 23:14:44.182  3314  4302 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-25 23:14:44.307  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:44.362  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-25 23:14:44.363  3314  4431 D GhDiag  : dns_reply 1133ms path=doh:cloudflare-dns.com bytes=274
10-25 23:14:44.497  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.523  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=257
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_reply 1361ms path=doh:cloudflare-dns.com bytes=260
10-25 23:14:45.119  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=471
10-25 23:14:45.121  3314  4431 D GhDiag  : dns_reply 1820ms path=doh:cloudflare-dns.com bytes=164
10-25 23:14:45.129  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.276  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:45.290  3314  4558 D GhDiag  : flow_established 13ms
10-25 23:14:45.314  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=192
10-25 23:14:45.342  3314  4552 D GhDiag  : flow_established 12ms
10-25 23:14:45.545  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=208
10-25 23:14:45.571  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.583  3314  4567 D GhDiag  : flow_established 7ms
10-25 23:14:45.825  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=233
10-25 23:14:46.292  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.544  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.560  3314  4579 D GhDiag  : flow_established 8ms
10-25 23:14:46.586  3314  4580 D GhDiag  : flow_established 6ms
10-25 23:14:46.840  3314  4581 D GhDiag  : flow_established 178ms
10-25 23:14:47.041  3314  4301 D GhDiag  : stats t=5s packets=118 tcp=94 dns53=8 otherUdp=6 activeTcp=8 flowsOpened=9 flowsEstablished=9 connectFailures=0 retransmits=0 appUp=52111 appDown=9490 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:14:47.250  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5203
10-25 23:14:47.858  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:47.870  3314  4626 D GhDiag  : flow_established 3ms
10-25 23:14:48.304  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-25 23:14:48.358  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:48.458  3314  4655 D GhDiag  : flow_established 81ms
10-25 23:14:48.490  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=161
10-25 23:14:48.553  3314  4302 D GhDiag  : flow_open 142.251.x.x:443
10-25 23:14:48.607  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=230 down=0 ms=6173
10-25 23:14:48.701  3314  4667 D GhDiag  : flow_established 45ms
10-25 23:14:48.818  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.029  3314  4677 D GhDiag  : flow_established 45ms
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 23:14:35.562  3314  3314 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 23:14:35.563  3314  3314 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 23:14:35.909  3314  3314 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 23:14:36.034  3314  3314 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:14:36.034  3314  3314 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:14:36.034  3314  3314 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 23:14:36.274  3314  3314 D GhDiag  : connect: core.start=true 
10-25 23:14:42.036  3314  3314 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.047  3314  4303 D GhDiag  : flow_open 1.1.x.x:80
10-25 23:14:42.074  3314  4308 D GhDiag  : flow_established 10ms
10-25 23:14:42.186  3314  4303 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=29 firstByteMs=84 checksums=0
10-25 23:14:42.352  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.353  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.434  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-25 23:14:42.434  3314  4302 D GhDiag  : flow_open fd00:1:…:853
10-25 23:14:42.476  3314  4327 D GhDiag  : flow_established 18ms
10-25 23:14:42.484  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:42.484  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=290
10-25 23:14:43.046  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.046  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.131  3314  4302 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:14:43.131  3314  4302 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:14:43.166  3314  4302 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-25 23:14:43.191  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.219  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.219  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:14:43.230  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:14:43.282  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:14:43.301  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:14:43.445  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-25 23:14:43.445  3314  4302 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:14:43.489  3314  4450 D GhDiag  : flow_established 2ms
10-25 23:14:43.490  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=40
10-25 23:14:43.491  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=270
10-25 23:14:43.539  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.682  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.683  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.789  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=560
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_reply 579ms path=doh:cloudflare-dns.com bytes=178
10-25 23:14:44.182  3314  4302 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-25 23:14:44.307  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:44.362  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-25 23:14:44.363  3314  4431 D GhDiag  : dns_reply 1133ms path=doh:cloudflare-dns.com bytes=274
10-25 23:14:44.497  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.523  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=257
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_reply 1361ms path=doh:cloudflare-dns.com bytes=260
10-25 23:14:45.119  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=471
10-25 23:14:45.121  3314  4431 D GhDiag  : dns_reply 1820ms path=doh:cloudflare-dns.com bytes=164
10-25 23:14:45.129  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.276  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:45.290  3314  4558 D GhDiag  : flow_established 13ms
10-25 23:14:45.314  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=192
10-25 23:14:45.342  3314  4552 D GhDiag  : flow_established 12ms
10-25 23:14:45.545  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=208
10-25 23:14:45.571  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.583  3314  4567 D GhDiag  : flow_established 7ms
10-25 23:14:45.825  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=233
10-25 23:14:46.292  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.544  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.560  3314  4579 D GhDiag  : flow_established 8ms
10-25 23:14:46.586  3314  4580 D GhDiag  : flow_established 6ms
10-25 23:14:46.840  3314  4581 D GhDiag  : flow_established 178ms
10-25 23:14:47.041  3314  4301 D GhDiag  : stats t=5s packets=118 tcp=94 dns53=8 otherUdp=6 activeTcp=8 flowsOpened=9 flowsEstablished=9 connectFailures=0 retransmits=0 appUp=52111 appDown=9490 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:14:47.250  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5203
10-25 23:14:47.858  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:47.870  3314  4626 D GhDiag  : flow_established 3ms
10-25 23:14:48.304  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-25 23:14:48.358  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:48.458  3314  4655 D GhDiag  : flow_established 81ms
10-25 23:14:48.490  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=161
10-25 23:14:48.553  3314  4302 D GhDiag  : flow_open 142.251.x.x:443
10-25 23:14:48.607  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=230 down=0 ms=6173
10-25 23:14:48.701  3314  4667 D GhDiag  : flow_established 45ms
10-25 23:14:48.818  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.029  3314  4677 D GhDiag  : flow_established 45ms
10-25 23:14:49.257  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.303  3314  4689 D GhDiag  : flow_established 3ms
10-25 23:14:49.850  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.864  3314  4712 D GhDiag  : flow_established 2ms
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
Using CollectorTypeCC GC.
10-25 23:14:27.628  3314  3314 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 23:14:27.628  3314  3314 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 23:14:27.831  3314  3314 W ziparchive: Unable to open '/data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/base.dm': No such file or directory
10-25 23:14:27.831  3314  3314 W ziparchive: Unable to open '/data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/base.dm': No such file or directory
10-25 23:14:28.041  3314  3314 D nativeloader: Configuring clns-6 for other apk /data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/lib/x86_64:/data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 23:14:28.051  3314  3314 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 23:14:28.051  3314  3314 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 23:14:28.827  3314  3314 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 23:14:28.827  3314  3314 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 23:14:28.827  3314  3314 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 23:14:28.827  3314  3314 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 23:14:28.827  3314  3314 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 23:14:28.828  3314  3314 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 23:14:28.828  3314  3314 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 23:14:29.859   524  2753 D CoreBackPreview: Window{ad4c5f1 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@a4eb758, mPriority=0, mIsAnimationCallback=false}
10-25 23:14:31.578   524  2754 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{294c7a9 com.google.android.gm/10140} BLOCKED
10-25 23:14:31.630  1625  1625 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 23:14:31.968   524   541 W ziparchive: Unable to open '/data/app/~~0ukFKJUOMxQc_zhyO9hWIg==/com.ghprotocol.app-W3Kdvfih6vhyBFvzebOcgw==/base.dm': No such file or directory
10-25 23:14:31.968   524   541 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +5s135ms
10-25 23:14:32.010   524  1969 W InputManager-JNI: Input channel object '67ca8fb Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 23:14:32.011   524   538 D CoreBackPreview: Window{67ca8fb u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 23:14:34.099   524   622 I InputDispatcher: ad4c5f1 com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2104ms processing FocusEvent(hasFocus=true)
10-25 23:14:34.116   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{93ebe2a com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{c23f41b com.android.camera2/10146} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{79159b8 com.google.android.gm/10140} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{e897391 com.google.android.devicelockcontroller/10179} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{4e292f6 com.google.android.dialer/10128} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{d83b6f7 com.google.android.contacts/10155} BLOCKED
10-25 23:14:34.117   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{cde5964 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 23:14:34.172   524  2721 I ImeTracker: com.ghprotocol.app:4190ee3d: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 23:14:34.173   524  2721 I ImeTracker: com.ghprotocol.app:4190ee3d: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:14:34.188  1524  1524 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:14:34.564  3314  3843 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 23:14:35.068   524  2754 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 23:14:35.097   832   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@826fa72 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=55467 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@f138ec3} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{ea56340 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:14:35.285  3908  3908 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 23:14:35.289  3908  3908 I AndroidRuntime: Using default boot image
10-25 23:14:35.289  3908  3908 I AndroidRuntime: Leaving lock profiling enabled
10-25 23:14:35.473  3908  3908 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 23:14:35.562  3314  3314 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 23:14:35.563  3314  3314 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 23:14:35.703  3974  3974 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:14:35.703  3974  3974 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:14:35.703  3974  3974 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:14:35.703  3974  3974 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 23:14:35.909  3314  3314 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 23:14:36.034  3314  3314 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:14:36.034  3314  3314 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-25 23:14:36.034  3314  3314 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 23:14:36.274  3314  3314 D GhDiag  : connect: core.start=true 
10-25 23:14:36.278   524   593 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{fe454d4 com.google.android.settings.intelligence/10118} BLOCKED
10-25 23:14:36.332   524   593 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{b1f54f6 com.google.android.settings.intelligence/10118} BLOCKED
10-25 23:14:36.657  3908  3908 D AndroidRuntime: Shutting down VM
10-25 23:14:36.930   524  1969 D CoreBackPreview: Window{d6ff1c9 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@6c3ec8f, mPriority=0, mIsAnimationCallback=false}
10-25 23:14:37.047  4038  4038 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=55879 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 23:14:37.730   524   541 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +2s664ms
10-25 23:14:37.730   524   541 V WindowManager: Sent Transition #7 createdAt=10-25 23:14:35.049 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=55467 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{911d6ab Task{bd77222 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{fa9d5f3 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:14:37.731   832   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@826fa72: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{2a755c3 u0 com.ghprotocol.app/.MainActivity)/@0x428f279 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4cee3ed u0 com.ghprotocol.app/.MainActivity)/@0x1e64bbe sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:14:37.732   832   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{2a755c3 u0 com.ghprotocol.app/.MainActivity)/@0x428f279 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4cee3ed u0 com.ghprotocol.app/.MainActivity)/@0x1e64bbe sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:14:37.732   832   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{2a755c3 u0 com.ghprotocol.app/.MainActivity)/@0x428f279 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4cee3ed u0 com.ghprotocol.app/.MainActivity)/@0x1e64bbe sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:14:37.741   524   541 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{2a755c3 u0 com.ghprotocol.app/.MainActivity)/@0x332632d sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4cee3ed u0 com.ghprotocol.app/.MainActivity)/@0x1e81644 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 23:14:38.301  3314  3336 I .ghprotocol.app: Background concurrent copying GC freed 100980(5319KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6581KB/12MB, paused 49us,5us total 661.587ms
10-25 23:14:38.309   832   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@4e5aeb3 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=58153 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@2781c70} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{46e6be9 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:14:38.373   524  2721 I ImeTracker: com.ghprotocol.app:dd0d35a0: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 23:14:38.374   524  2721 I ImeTracker: com.ghprotocol.app:dd0d35a0: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:14:38.376  1524  1524 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:14:38.414  4165  4165 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 23:14:38.418   524  2721 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 23:14:38.424  4165  4165 I AndroidRuntime: Using default boot image
10-25 23:14:38.424  4165  4165 I AndroidRuntime: Leaving lock profiling enabled
10-25 23:14:38.425   524  2721 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 23:14:38.425   524  2721 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 23:14:38.683  4165  4165 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 23:14:39.573   524   541 V WindowManager: Sent Transition #8 createdAt=10-25 23:14:37.740 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=58153 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{911d6ab Task{bd77222 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b250890 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 23:14:40.166  4165  4165 D AndroidRuntime: Shutting down VM
10-25 23:14:41.376   524   593 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 23:14:41.503  1446  3195 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 23:14:41.809  1398  3960 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 23:14:41.846   524  2740 I ImeTracker: com.ghprotocol.app:2ff3ffdc: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 23:14:41.847   524  2740 I ImeTracker: com.ghprotocol.app:2ff3ffdc: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 23:14:41.850  1524  1524 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 23:14:41.988   524  2740 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 23:14:42.035   524  2756 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 23:14:42.036  3314  3314 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-25 23:14:42.041  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.047  3314  4303 D GhDiag  : flow_open 1.1.x.x:80
10-25 23:14:42.074  3314  4308 D GhDiag  : flow_established 10ms
10-25 23:14:42.186  3314  4303 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=29 firstByteMs=84 checksums=0
10-25 23:14:42.352  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.353  3314  4302 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-25 23:14:42.434  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-25 23:14:42.434  3314  4302 D GhDiag  : flow_open fd00:1:…:853
10-25 23:14:42.476  3314  4327 D GhDiag  : flow_established 18ms
10-25 23:14:42.484  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:42.484  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=290
10-25 23:14:42.851  3314  3335 I .ghprotocol.app: Compiler allocated 4270KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 23:14:43.046  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.046  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.131  3314  4302 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:14:43.131  3314  4302 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-25 23:14:43.166  3314  4302 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-25 23:14:43.191  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.219  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.219  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:14:43.230  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-25 23:14:43.282  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:14:43.301  3314  4302 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-25 23:14:43.445  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-25 23:14:43.445  3314  4302 D GhDiag  : flow_open 10.8.x.x:853
10-25 23:14:43.489  3314  4450 D GhDiag  : flow_established 2ms
10-25 23:14:43.490  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=40
10-25 23:14:43.491  3314  4302 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=270
10-25 23:14:43.539  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.682  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.683  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:43.750  3314  3336 I .ghprotocol.app: Background young concurrent copying GC freed 81487(5354KB) AllocSpace objects, 2(40KB) LOS objects, 36% free, 8321KB/12MB, paused 148us,28us total 256.520ms
10-25 23:14:43.789  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=560
10-25 23:14:43.799  3314  4431 D GhDiag  : dns_reply 579ms path=doh:cloudflare-dns.com bytes=178
10-25 23:14:44.106  1625  1625 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 23:14:44.106  1625  2419 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 23:14:44.106  1625  2419 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 23:14:44.182  3314  4302 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-25 23:14:44.280   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{544e50 com.google.android.apps.messaging/10130} BLOCKED
10-25 23:14:44.280   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{5a1e849 com.google.android.gm/10140} BLOCKED
10-25 23:14:44.280   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{c2c554e com.google.android.rkpdapp/10178} BLOCKED
10-25 23:14:44.282   524   575 I AppsFilter: interaction: PackageSetting{b938f30 com.ghprotocol.app/10192} -> PackageSetting{d9484d5 com.google.android.projection.gearhead/10123} BLOCKED
10-25 23:14:44.307  3314  4302 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=60
10-25 23:14:44.362  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-25 23:14:44.363  3314  4431 D GhDiag  : dns_reply 1133ms path=doh:cloudflare-dns.com bytes=274
10-25 23:14:44.497  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.523  3314  4302 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=257
10-25 23:14:44.643  3314  4431 D GhDiag  : dns_reply 1361ms path=doh:cloudflare-dns.com bytes=260
10-25 23:14:45.119  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=471
10-25 23:14:45.121  3314  4431 D GhDiag  : dns_reply 1820ms path=doh:cloudflare-dns.com bytes=164
10-25 23:14:45.129  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.276  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:45.290  3314  4558 D GhDiag  : flow_established 13ms
10-25 23:14:45.314  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=192
10-25 23:14:45.342  3314  4552 D GhDiag  : flow_established 12ms
10-25 23:14:45.545  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=208
10-25 23:14:45.571  3314  4302 D GhDiag  : flow_open 172.217.x.x:443
10-25 23:14:45.583  3314  4567 D GhDiag  : flow_established 7ms
10-25 23:14:45.825  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=233
10-25 23:14:46.292  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.353  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.544  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:46.560  3314  4579 D GhDiag  : flow_established 8ms
10-25 23:14:46.586  3314  4580 D GhDiag  : flow_established 6ms
10-25 23:14:46.840  3314  4581 D GhDiag  : flow_established 178ms
10-25 23:14:46.881  3314  3336 W .ghprotocol.app: Suspending all threads took: 10.089ms
10-25 23:14:46.882  3314  3336 I .ghprotocol.app: Background young concurrent copying GC freed 74655(5155KB) AllocSpace objects, 0(0B) LOS objects, 32% free, 8928KB/12MB, paused 96us,10.140ms total 350.908ms
10-25 23:14:47.041  3314  4301 D GhDiag  : stats t=5s packets=118 tcp=94 dns53=8 otherUdp=6 activeTcp=8 flowsOpened=9 flowsEstablished=9 connectFailures=0 retransmits=0 appUp=52111 appDown=9490 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-25 23:14:47.250  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=91 down=402 ms=5203
10-25 23:14:47.858  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:47.870  3314  4626 D GhDiag  : flow_established 3ms
10-25 23:14:48.304  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-25 23:14:48.358  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:48.458  3314  4655 D GhDiag  : flow_established 81ms
10-25 23:14:48.490  3314  4431 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=161
10-25 23:14:48.553  3314  4302 D GhDiag  : flow_open 142.251.x.x:443
10-25 23:14:48.607  3314  4307 D GhDiag  : flow_closed reason=half_close_complete up=230 down=0 ms=6173
10-25 23:14:48.701  3314  4667 D GhDiag  : flow_established 45ms
10-25 23:14:48.818  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.029  3314  4677 D GhDiag  : flow_established 45ms
10-25 23:14:49.257  3314  4302 D GhDiag  : flow_open 2001:4860:…:443
10-25 23:14:49.303  3314  4689 D GhDiag  : flow_established 3ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
