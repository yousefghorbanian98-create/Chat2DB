## gh-protocol E2E log — 2026-10-26T01:03:13Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-26T01:01:47Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 26 00:58 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 26 01:02 .
drwxr-xr-x 3 runner runner 4096 Oct 26 01:02 ..
drwxr-xr-x 3 runner runner 4096 Oct 26 01:02 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 26 01:02 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2810
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
WARNING: cannnot unmap ptr 0x7f50b9601000 as it is in the protected range from 0x7f4fb9600000 to 0x7f50b9800000
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
INFO         | Boot completed in 29687 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
INFO         | Wait for emulator (pid 2810) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:45969 is gone due to Stream removed (CANCELLED)

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
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResValues
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:mergeLibDexDebug
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792976349456.json

BUILD SUCCESSFUL in 2m 16s
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
app up (try 1, pid 3125)
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
    inet6 fe80::cb36:dd94:5232:5463/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.4): 56(84) bytes.

--- 140.82.114.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
relay self-test PASS (real remote payload through the relay)
10-26 01:03:04.254  3125  4410 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=26 firstByteMs=70 checksums=0
10-26 01:03:04.729  3125  4430 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=60 firstByteMs=269 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-26 01:03:05.086  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.116  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=323
10-26 01:03:05.121  3125  4429 D GhDiag  : dns_reply 780ms path=doh:cloudflare-dns.com bytes=269
10-26 01:03:05.130  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:05.290  3125  4409 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:03:05.326  3125  4409 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:03:05.326  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:33496->10.8.x.x:853
10-26 01:03:05.336  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:33496->10.8.0.1:853
10-26 01:03:05.499  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=216
10-26 01:03:05.502  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=899
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.683  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-26 01:03:05.684  3125  4429 D GhDiag  : dns_reply 1156ms path=doh:cloudflare-dns.com bytes=257
10-26 01:03:05.852  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:03:05.854  3125  4429 D GhDiag  : dns_reply 1324ms path=doh:cloudflare-dns.com bytes=49
10-26 01:03:05.863  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:03:05.864  3125  4409 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:03:05.893  3125  4488 D GhDiag  : flow_established 2ms
10-26 01:03:05.895  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.903  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=221
10-26 01:03:05.964  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.108  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=253
10-26 01:03:06.137  3125  4429 D GhDiag  : dns_reply 592ms path=doh:cloudflare-dns.com bytes=260
10-26 01:03:06.142  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.144  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.236  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=99
10-26 01:03:06.237  3125  4429 D GhDiag  : dns_reply 692ms path=doh:cloudflare-dns.com bytes=164
10-26 01:03:06.241  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.280  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.366  3125  4492 D GhDiag  : flow_established 60ms
10-26 01:03:06.384  3125  4501 D GhDiag  : flow_established 7ms
10-26 01:03:07.487  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=85
10-26 01:03:07.595  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=107
10-26 01:03:07.612  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:07.668  3125  4571 D GhDiag  : flow_established 51ms
10-26 01:03:08.440  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.457  3125  4600 D GhDiag  : flow_established 6ms
10-26 01:03:08.458  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.469  3125  4603 D GhDiag  : flow_established 5ms
10-26 01:03:09.183  3125  4408 D GhDiag  : stats t=5s packets=112 tcp=85 dns53=8 otherUdp=9 activeTcp=6 flowsOpened=8 flowsEstablished=8 connectFailures=0 retransmits=0 appUp=32441 appDown=58275 probeUp=182 probeDown=804 probeFlows=2 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-26 01:03:09.273  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5061 probe=true
10-26 01:03:09.315  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.323  3125  4613 D GhDiag  : flow_established 7ms
10-26 01:03:09.596  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.659  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:09.679  3125  4627 D GhDiag  : flow_established 25ms
10-26 01:03:09.702  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-26 01:03:09.717  3125  4633 D GhDiag  : flow_established 49ms
10-26 01:03:09.810  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41001->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5352 probe=true
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=32441 bytes
10-26 01:03:09.183  3125  4408 D GhDiag  : stats t=5s packets=112 tcp=85 dns53=8 otherUdp=9 activeTcp=6 flowsOpened=8 flowsEstablished=8 connectFailures=0 retransmits=0 appUp=32441 appDown=58275 probeUp=182 probeDown=804 probeFlows=2 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
tunnel-local destinations are reset locally (no wasted upstream dial)
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-26 01:02:57.008  3125  3125 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:02:57.008  3125  3125 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:02:57.225  3125  3125 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:02:57.289  3125  3125 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:02:57.289  3125  3125 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:02:57.290  3125  3125 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:02:57.427  3125  3125 D GhDiag  : connect: core.start=true 
10-26 01:03:04.137  3125  3125 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:04.204  3125  4410 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:03:04.207  3125  4413 D GhDiag  : flow_established 3ms
10-26 01:03:04.254  3125  4410 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=26 firstByteMs=70 checksums=0
10-26 01:03:04.301  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.301  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58234->fd00:1:…:853
10-26 01:03:04.310  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58234->fd00:1::1:853
10-26 01:03:04.315  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.316  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58238->fd00:1:…:853
10-26 01:03:04.316  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58238->fd00:1::1:853
10-26 01:03:04.339  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=73
10-26 01:03:04.341  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=73
10-26 01:03:04.357  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.250.x.x:443 len=61
10-26 01:03:04.384  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:04.396  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:03:04.397  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.250.x.x:443 len=79
10-26 01:03:04.458  3125  4430 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:03:04.511  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:03:04.529  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:03:04.529  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.529  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58250->fd00:1:…:853
10-26 01:03:04.530  3125  4431 D GhDiag  : flow_established 28ms
10-26 01:03:04.530  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58250->fd00:1::1:853
10-26 01:03:04.640  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:04.729  3125  4430 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=60 firstByteMs=269 checksums=0
10-26 01:03:04.790  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=434
10-26 01:03:04.792  3125  4429 D GhDiag  : dns_reply 453ms path=doh:cloudflare-dns.com bytes=173
10-26 01:03:05.064  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:05.086  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.116  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=323
10-26 01:03:05.121  3125  4429 D GhDiag  : dns_reply 780ms path=doh:cloudflare-dns.com bytes=269
10-26 01:03:05.130  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:05.290  3125  4409 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:03:05.326  3125  4409 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:03:05.326  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:33496->10.8.x.x:853
10-26 01:03:05.336  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:33496->10.8.0.1:853
10-26 01:03:05.499  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=216
10-26 01:03:05.502  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=899
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.683  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-26 01:03:05.684  3125  4429 D GhDiag  : dns_reply 1156ms path=doh:cloudflare-dns.com bytes=257
10-26 01:03:05.852  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:03:05.854  3125  4429 D GhDiag  : dns_reply 1324ms path=doh:cloudflare-dns.com bytes=49
10-26 01:03:05.863  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:03:05.864  3125  4409 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:03:05.893  3125  4488 D GhDiag  : flow_established 2ms
10-26 01:03:05.895  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.903  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=221
10-26 01:03:05.964  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.108  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=253
10-26 01:03:06.137  3125  4429 D GhDiag  : dns_reply 592ms path=doh:cloudflare-dns.com bytes=260
10-26 01:03:06.142  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.144  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.236  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=99
10-26 01:03:06.237  3125  4429 D GhDiag  : dns_reply 692ms path=doh:cloudflare-dns.com bytes=164
10-26 01:03:06.241  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.280  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.366  3125  4492 D GhDiag  : flow_established 60ms
10-26 01:03:06.384  3125  4501 D GhDiag  : flow_established 7ms
10-26 01:03:07.487  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=85
10-26 01:03:07.595  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=107
10-26 01:03:07.612  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:07.668  3125  4571 D GhDiag  : flow_established 51ms
10-26 01:03:08.440  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.457  3125  4600 D GhDiag  : flow_established 6ms
10-26 01:03:08.458  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.469  3125  4603 D GhDiag  : flow_established 5ms
10-26 01:03:09.183  3125  4408 D GhDiag  : stats t=5s packets=112 tcp=85 dns53=8 otherUdp=9 activeTcp=6 flowsOpened=8 flowsEstablished=8 connectFailures=0 retransmits=0 appUp=32441 appDown=58275 probeUp=182 probeDown=804 probeFlows=2 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-26 01:03:09.273  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5061 probe=true
10-26 01:03:09.315  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.323  3125  4613 D GhDiag  : flow_established 7ms
10-26 01:03:09.596  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.659  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:09.679  3125  4627 D GhDiag  : flow_established 25ms
10-26 01:03:09.702  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-26 01:03:09.717  3125  4633 D GhDiag  : flow_established 49ms
10-26 01:03:09.810  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41001->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5352 probe=true
10-26 01:03:09.857  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=141
10-26 01:03:09.862  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:10.062  3125  4647 D GhDiag  : flow_established 66ms
10-26 01:03:10.216  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=358
10-26 01:03:10.365  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:10.461  3125  4660 D GhDiag  : flow_established 6ms
10-26 01:03:10.714  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=497
10-26 01:03:10.726  3125  4409 D GhDiag  : flow_open v4 dst=142.250.x.x:443 probe=false
10-26 01:03:10.799  3125  4684 D GhDiag  : flow_established 23ms
10-26 01:03:10.892  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:10.934  3125  4691 D GhDiag  : flow_established 6ms
10-26 01:03:11.581  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=184
10-26 01:03:11.700  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=109
10-26 01:03:11.730  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
tocol.app/10192} -> PackageSetting{7420c68 com.google.android.dialer/10128} BLOCKED
10-26 01:02:50.088   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{7572881 com.google.android.contacts/10155} BLOCKED
10-26 01:02:50.088   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{339bd26 com.google.android.partnersetup/10124} BLOCKED
10-26 01:02:50.088   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{89b4d67 com.google.android.apps.youtube.music/10156} BLOCKED
10-26 01:02:50.088   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{5f8714 com.google.android.cellbroadcastreceiver/10184} BLOCKED
10-26 01:02:50.106   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{2a6b575 com.google.android.inputmethod.latin/10144} BLOCKED
10-26 01:02:50.108  1042  1356 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-26 01:02:50.111  1042  1042 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-26 01:02:50.126  1042  1356 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-26 01:02:50.234  3125  3125 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-26 01:02:50.234  3125  3125 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-26 01:02:50.234  3125  3125 W .ghprotocol.app: and incorrect proguard optimizations.
10-26 01:02:50.234  3125  3125 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-26 01:02:50.234  3125  3125 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-26 01:02:50.239  3125  3125 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-26 01:02:50.239  3125  3125 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-26 01:02:50.680   526  2764 D CoreBackPreview: Window{57a817c u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@ee8677f, mPriority=0, mIsAnimationCallback=false}
10-26 01:02:52.128   526   543 W ziparchive: Unable to open '/data/app/~~5TDHGldFw52PFnL9MehBNQ==/com.ghprotocol.app-POFnVczQ8e6EKZvhD5_hEg==/base.dm': No such file or directory
10-26 01:02:52.143   526   543 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s881ms
10-26 01:02:52.184   526   539 D CoreBackPreview: Window{6ef92a1 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-26 01:02:52.184   526  1152 W InputManager-JNI: Input channel object '6ef92a1 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-26 01:02:54.691   526   622 I InputDispatcher: 57a817c com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2553ms processing FocusEvent(hasFocus=true)
10-26 01:02:54.731   526   902 I ImeTracker: com.ghprotocol.app:730af666: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:02:54.732   526   902 I ImeTracker: com.ghprotocol.app:730af666: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:02:54.751  1529  1529 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:02:55.666  3125  3891 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-26 01:02:55.910   526  2551 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{fed4999 com.google.android.gm/10143} BLOCKED
10-26 01:02:56.171  1585  1585 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-26 01:02:56.596  1585  1585 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-26 01:02:56.600  1585  2852 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-26 01:02:56.600  1585  2852 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-26 01:02:56.695   526   902 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-26 01:02:56.697   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@aa96a57 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=44483 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@ed2f944} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{65f0a2d com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:02:56.723  3125  3125 V ActivityThread: getPackageInfo() caused update to cached ApplicationInfo for package com.ghprotocol.app
10-26 01:02:56.876  3962  3962 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:02:56.880  3962  3962 I AndroidRuntime: Using default boot image
10-26 01:02:56.880  3962  3962 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:02:57.008  3125  3125 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:02:57.008  3125  3125 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:02:57.034  3962  3962 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:02:57.070  3991  3991 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:02:57.074  3991  3991 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-26 01:02:57.225  3125  3125 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:02:57.289  3125  3125 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:02:57.289  3125  3125 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:02:57.290  3125  3125 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:02:57.427  3125  3125 D GhDiag  : connect: core.start=true 
10-26 01:02:57.585   526   916 D CoreBackPreview: Window{b5a39a u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@708b568, mPriority=0, mIsAnimationCallback=false}
10-26 01:02:58.408   834   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@aa96a57: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{9c868e1 u0 com.ghprotocol.app/.MainActivity)/@0xfb74fd2 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{d2f3cec u0 com.ghprotocol.app/.MainActivity)/@0x9cb28a3 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:02:58.409   526   543 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s724ms
10-26 01:02:58.409   526   543 V WindowManager: Sent Transition #7 createdAt=10-26 01:02:56.686 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=44483 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{4b13d46 Task{c3508b5 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{cbf7a24 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:02:58.409   526   543 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{9c868e1 u0 com.ghprotocol.app/.MainActivity)/@0x3c715b6 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{d2f3cec u0 com.ghprotocol.app/.MainActivity)/@0xf774951 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:02:58.410   834   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{9c868e1 u0 com.ghprotocol.app/.MainActivity)/@0xfb74fd2 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{d2f3cec u0 com.ghprotocol.app/.MainActivity)/@0x9cb28a3 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:02:58.413   834   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{9c868e1 u0 com.ghprotocol.app/.MainActivity)/@0xfb74fd2 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{d2f3cec u0 com.ghprotocol.app/.MainActivity)/@0x9cb28a3 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:02:58.585  3125  3145 I .ghprotocol.app: Background concurrent copying GC freed 105848(5460KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6993KB/13MB, paused 24us,3.529ms total 207.672ms
10-26 01:02:58.825  3962  3962 D AndroidRuntime: Shutting down VM
10-26 01:02:58.908   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@4513b68 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=46246 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@1202b81} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{eba0426 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:02:59.461   526   886 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-26 01:02:59.465   526   886 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-26 01:02:59.465   526   886 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-26 01:02:59.711  1445  3709 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-26 01:02:59.816  1402  3998 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-26 01:03:00.135   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{ad38d43 com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:03:00.139   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{5efbfc0 com.android.camera2/10146} BLOCKED
10-26 01:03:00.139   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{20154f9 com.google.android.devicelockcontroller/10190} BLOCKED
10-26 01:03:00.139   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{40b3c3e com.google.android.rkpdapp/10186} BLOCKED
10-26 01:03:00.139   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{6c0de53 com.google.android.projection.gearhead/10123} BLOCKED
10-26 01:03:00.139   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{b17ba9f com.google.android.apps.youtube.music/10156} BLOCKED
10-26 01:03:00.239   526   543 V WindowManager: Sent Transition #8 createdAt=10-26 01:02:58.449 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=46246 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{4b13d46 Task{c3508b5 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b78eca2 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:03:00.956  4274  4274 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:03:00.962  4274  4274 I AndroidRuntime: Using default boot image
10-26 01:03:00.963  4274  4274 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:03:01.155  4274  4274 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:03:02.597  4274  4274 D AndroidRuntime: Shutting down VM
10-26 01:03:03.862   526  2681 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-26 01:03:04.108   526  2574 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-26 01:03:04.136   526  1407 I Vpn     : Established by com.ghprotocol.app on tun0
10-26 01:03:04.137  3125  3125 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 dns=10.8.0.1 mtu=1500
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:03:04.192  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:04.204  3125  4410 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:03:04.207  3125  4413 D GhDiag  : flow_established 3ms
10-26 01:03:04.254  3125  4410 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=26 firstByteMs=70 checksums=0
10-26 01:03:04.301  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.301  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58234->fd00:1:…:853
10-26 01:03:04.310  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58234->fd00:1::1:853
10-26 01:03:04.315  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.316  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58238->fd00:1:…:853
10-26 01:03:04.316  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58238->fd00:1::1:853
10-26 01:03:04.339  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=73
10-26 01:03:04.341  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=73
10-26 01:03:04.357  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.250.x.x:443 len=61
10-26 01:03:04.384  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:04.396  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:03:04.397  3125  4409 D GhDiag  : tun v4 proto=17 dst=142.250.x.x:443 len=79
10-26 01:03:04.415   526  2551 I ImeTracker: com.ghprotocol.app:adb9c762: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:03:04.415   526  2551 I ImeTracker: com.ghprotocol.app:adb9c762: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:03:04.426  1529  1529 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:03:04.458  3125  4430 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:03:04.511  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:03:04.529  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-26 01:03:04.529  3125  4409 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:03:04.529  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:58250->fd00:1:…:853
10-26 01:03:04.530  3125  4431 D GhDiag  : flow_established 28ms
10-26 01:03:04.530  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:58250->fd00:1::1:853
10-26 01:03:04.640  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:04.729  3125  4430 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=60 firstByteMs=269 checksums=0
10-26 01:03:04.790  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=434
10-26 01:03:04.792  3125  4429 D GhDiag  : dns_reply 453ms path=doh:cloudflare-dns.com bytes=173
10-26 01:03:05.043  3125  3144 I .ghprotocol.app: Compiler allocated 4270KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-26 01:03:05.064  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:05.070  3125  3145 I .ghprotocol.app: Background young concurrent copying GC freed 102425(5934KB) AllocSpace objects, 2(40KB) LOS objects, 37% free, 8744KB/13MB, paused 326us,12us total 208.105ms
10-26 01:03:05.086  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.116  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=323
10-26 01:03:05.121  3125  4429 D GhDiag  : dns_reply 780ms path=doh:cloudflare-dns.com bytes=269
10-26 01:03:05.130  3125  4409 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:03:05.290  3125  4409 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-26 01:03:05.326  3125  4409 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:03:05.326  3125  4409 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:33496->10.8.x.x:853
10-26 01:03:05.336  3125  4409 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:33496->10.8.0.1:853
10-26 01:03:05.499  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=216
10-26 01:03:05.502  3125  4409 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=899
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.545  3125  4409 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-26 01:03:05.683  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=551
10-26 01:03:05.684  3125  4429 D GhDiag  : dns_reply 1156ms path=doh:cloudflare-dns.com bytes=257
10-26 01:03:05.758  3125  3145 I .ghprotocol.app: Background concurrent copying GC freed 91404(7373KB) AllocSpace objects, 19(380KB) LOS objects, 49% free, 9231KB/18MB, paused 62us,15us total 208.839ms
10-26 01:03:05.852  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=167
10-26 01:03:05.854  3125  4429 D GhDiag  : dns_reply 1324ms path=doh:cloudflare-dns.com bytes=49
10-26 01:03:05.863  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:03:05.864  3125  4409 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:03:05.893  3125  4488 D GhDiag  : flow_established 2ms
10-26 01:03:05.895  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:05.903  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=221
10-26 01:03:05.964  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.108  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=253
10-26 01:03:06.137  3125  4429 D GhDiag  : dns_reply 592ms path=doh:cloudflare-dns.com bytes=260
10-26 01:03:06.142  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.144  3125  4409 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:03:06.236  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=99
10-26 01:03:06.237  3125  4429 D GhDiag  : dns_reply 692ms path=doh:cloudflare-dns.com bytes=164
10-26 01:03:06.241  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.280  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:06.366  3125  4492 D GhDiag  : flow_established 60ms
10-26 01:03:06.368  3125  3145 I .ghprotocol.app: Background young concurrent copying GC freed 118043(10212KB) AllocSpace objects, 0(0B) LOS objects, 47% free, 9665KB/18MB, paused 30us,17us total 190.722ms
10-26 01:03:06.384  3125  4501 D GhDiag  : flow_established 7ms
10-26 01:03:07.487  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=85
10-26 01:03:07.595  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=107
10-26 01:03:07.612  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:07.668  3125  4571 D GhDiag  : flow_established 51ms
10-26 01:03:08.440  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.457  3125  4600 D GhDiag  : flow_established 6ms
10-26 01:03:08.458  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:08.469  3125  4603 D GhDiag  : flow_established 5ms
10-26 01:03:09.183  3125  4408 D GhDiag  : stats t=5s packets=112 tcp=85 dns53=8 otherUdp=9 activeTcp=6 flowsOpened=8 flowsEstablished=8 connectFailures=0 retransmits=0 appUp=32441 appDown=58275 probeUp=182 probeDown=804 probeFlows=2 dnsOk=8 dnsFail=0 state=VERIFIED ipv6=tunneled
10-26 01:03:09.273  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5061 probe=true
10-26 01:03:09.315  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.323  3125  4613 D GhDiag  : flow_established 7ms
10-26 01:03:09.596  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:09.659  3125  4409 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:03:09.679  3125  4627 D GhDiag  : flow_established 25ms
10-26 01:03:09.702  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=110
10-26 01:03:09.717  3125  4633 D GhDiag  : flow_established 49ms
10-26 01:03:09.810  3125  4412 D GhDiag  : flow_closed dst=10.8.x.x:41001->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5352 probe=true
10-26 01:03:09.857  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=141
10-26 01:03:09.862  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:10.062  3125  4647 D GhDiag  : flow_established 66ms
10-26 01:03:10.216  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=358
10-26 01:03:10.365  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:03:10.461  3125  4660 D GhDiag  : flow_established 6ms
10-26 01:03:10.714  3125  4429 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=497
10-26 01:03:10.726  3125  4409 D GhDiag  : flow_open v4 dst=142.250.x.x:443 probe=false
10-26 01:03:10.795   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{cb8e69f com.google.android.gm/10143} BLOCKED
10-26 01:03:10.795   526   577 I AppsFilter: interaction: PackageSetting{bdb24e com.ghprotocol.app/10192} -> PackageSetting{ef8d3ec com.google.android.contacts/10155} BLOCKED
10-26 01:03:10.799  3125  4684 D GhDiag  : flow_established 23ms
10-26 01:03:10.832  3125  3145 I .ghprotocol.app: Background young concurrent copying GC freed 104919(8606KB) AllocSpace objects, 0(0B) LOS objects, 44% free, 9146KB/16MB, paused 18.884ms,27us total 305.349ms
10-26 01:03:10.892  3125  4409 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
