## gh-protocol E2E log — 2026-10-26T01:53:55Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-26T01:51:58Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 26 01:45 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 26 01:52 .
drwxr-xr-x 3 runner runner 4096 Oct 26 01:52 ..
drwxr-xr-x 3 runner runner 4096 Oct 26 01:52 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 26 01:52 gh_test.ini

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
ERROR        | Unable to connect to adb daemon on port: 5037
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3086
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
WARNING: cannnot unmap ptr 0x7f0eaa401000 as it is in the protected range from 0x7f0daa400000 to 0x7f0eaa600000
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
INFO         | Boot completed in 38247 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 114
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3086) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:36997 is gone due to Stream removed (CANCELLED)

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
> Task :app:mergeDebugShaders
> Task :app:packageDebugResources
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:validateSigningDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792979328953.json

BUILD SUCCESSFUL in 2m 56s
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
emulator can reach raw.githubusercontent.com after ~16s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3233)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 2)
tunnel up after ~8s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::2/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::3485:ede7:a2ae:bf16/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (172.182.252.133): 56(84) bytes.

--- 172.182.252.133 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
relay self-test PASS (real remote payload through the relay)
10-26 01:53:47.335  3233  4528 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:53:47.367  3233  4528 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=473 firstByteMs=544 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-26 01:53:41.615  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:41.623  3233  4692 D GhDiag  : flow_established 1ms
10-26 01:53:41.963  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=308
10-26 01:53:42.216  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=242
10-26 01:53:42.221  3233  4527 D GhDiag  : flow_open v4 dst=34.3.x.x:443 probe=false
10-26 01:53:42.262  3233  4716 D GhDiag  : flow_established 24ms
10-26 01:53:42.781  3233  4526 D GhDiag  : stats t=5s packets=109 tcp=69 dns53=12 otherUdp=13 activeTcp=5 flowsOpened=12 flowsEstablished=12 connectFailures=0 retransmits=0 appUp=5132 appDown=31526 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:53:42.819  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=180
10-26 01:53:42.941  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.040  3233  4735 D GhDiag  : flow_established 7ms
10-26 01:53:43.133  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.178  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=313
10-26 01:53:43.210  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:43.231  3233  4746 D GhDiag  : flow_established 30ms
10-26 01:53:43.359  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=170
10-26 01:53:43.442  3233  4750 D GhDiag  : flow_established 162ms
10-26 01:53:43.473  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=111
10-26 01:53:43.506  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.516  3233  4532 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5746 probe=true
10-26 01:53:43.682  3233  4761 D GhDiag  : flow_established 167ms
10-26 01:53:43.737  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.855  3233  4769 D GhDiag  : flow_established 2ms
10-26 01:53:44.075  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:44.097  3233  4772 D GhDiag  : flow_established 12ms
10-26 01:53:44.138  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:44.162  3233  4775 D GhDiag  : flow_established 8ms
10-26 01:53:44.196  3233  4527 D GhDiag  : flow_closed dst=10.8.x.x:56106->172.217.x.x:443 reason=client_rst up=0 down=0 ms=58 probe=false
10-26 01:53:44.917  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.016  3233  4781 D GhDiag  : flow_established 48ms
10-26 01:53:45.294  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.351  3233  4785 D GhDiag  : flow_established 35ms
10-26 01:53:46.585  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.620  3233  4797 D GhDiag  : flow_established 11ms
10-26 01:53:46.674  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.705  3233  4804 D GhDiag  : flow_established 28ms
10-26 01:53:46.747  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:46.899  3233  4807 D GhDiag  : flow_established 107ms
10-26 01:53:47.334  3233  4528 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:53:47.335  3233  4528 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:53:47.345  3233  4551 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:53:47.367  3233  4528 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=473 firstByteMs=544 checksums=0
10-26 01:53:47.517  3233  4810 D GhDiag  : flow_established 23ms
10-26 01:53:47.783  3233  4526 D GhDiag  : stats t=10s packets=792 tcp=743 dns53=12 otherUdp=17 activeTcp=16 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=77448 appDown=1653914 probeUp=182 probeDown=402 probeFlows=1 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:53:48.056  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49718->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6441 probe=false
10-26 01:53:48.162  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49122->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7429 probe=false
10-26 01:53:48.182  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48712->2001:4860:…:443
10-26 01:53:48.226  3233  4551 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:53:48.226  3233  4551 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:53:48.259  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48712->2001:4860:4842:400:::443
10-26 01:53:48.489  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:39774->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7337 probe=false
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=77448 bytes
10-26 01:53:47.783  3233  4526 D GhDiag  : stats t=10s packets=792 tcp=743 dns53=12 otherUdp=17 activeTcp=16 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=77448 appDown=1653914 probeUp=182 probeDown=402 probeFlows=1 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-26 01:53:47.335  3233  4528 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-26 01:53:27.778  3233  3233 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:53:27.784  3233  3233 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:53:28.140  3233  3233 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:53:28.275  3233  3233 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:53:28.277  3233  3233 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:53:28.277  3233  3233 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:53:28.414  3233  3233 D GhDiag  : connect: core.start=true 
10-26 01:53:37.660  3233  3233 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:53:37.769  3233  4528 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:53:37.776  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:53:37.777  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:53:37.777  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:38.206  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:38.241  3233  4533 D GhDiag  : flow_established 148ms
10-26 01:53:38.321  3233  4527 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:53:38.322  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47058->fd00:1:…:853
10-26 01:53:38.327  3233  4528 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:53:38.340  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47058->fd00:1::1:853
10-26 01:53:38.381  3233  4557 D GhDiag  : flow_established 17ms
10-26 01:53:38.463  3233  4527 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:53:38.470  3233  4527 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:53:38.470  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:53:38.504  3233  4527 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:53:38.505  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47060->fd00:1:…:853
10-26 01:53:38.507  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47060->fd00:1::1:853
10-26 01:53:38.510  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.510  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v4 proto=17 dst=10.0.x.x:53 len=60
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v4 proto=17 dst=10.0.x.x:53 len=60
10-26 01:53:38.532  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.533  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:38.674  3233  4527 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=130
10-26 01:53:38.674  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:53:38.706  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:38.735  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:53:38.736  3233  4562 D GhDiag  : flow_established 5ms
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.743  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:53:38.754  3233  4527 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=62
10-26 01:53:38.754  3233  4527 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=394
10-26 01:53:38.766  3233  4566 D GhDiag  : flow_established 8ms
10-26 01:53:38.769  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:53:38.782  3233  4563 D GhDiag  : flow_established 11ms
10-26 01:53:38.784  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.788  3233  4527 D GhDiag  : flow_closed dst=10.8.x.x:56226->142.251.x.x:443 reason=client_rst up=0 down=0 ms=110 probe=false
10-26 01:53:38.799  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=869
10-26 01:53:38.804  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=869
10-26 01:53:38.806  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.964  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:39.287  3233  4527 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=130
10-26 01:53:39.296  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:39.331  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47072->fd00:1:…:853
10-26 01:53:39.333  3233  4571 D GhDiag  : flow_established 223ms
10-26 01:53:39.365  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47072->fd00:1::1:853
10-26 01:53:39.365  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:39.486  3233  4598 D GhDiag  : flow_established 13ms
10-26 01:53:39.640  3233  4527 D GhDiag  : flow_closed dst=fd00:1:…:49108->2001:4860:…:443 reason=client_rst up=0 down=0 ms=827 probe=false
10-26 01:53:39.685  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:59616->10.8.x.x:853
10-26 01:53:39.697  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:59616->10.8.0.1:853
10-26 01:53:39.750  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:39.773  3233  4527 D GhDiag  : flow_closed dst=fd00:1:…:49114->2001:4860:…:443 reason=client_rst up=0 down=0 ms=408 probe=false
10-26 01:53:39.863  3233  4559 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:53:39.864  3233  4559 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1536 probe=false
10-26 01:53:39.926  3233  4608 D GhDiag  : flow_established 2ms
10-26 01:53:40.034  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=1488
10-26 01:53:40.088  3233  4565 D GhDiag  : flow_closed dst=fd00:1:…:58298->2001:4860:…:443 reason=upstream_eof up=809 down=0 ms=1555 probe=false
10-26 01:53:40.089  3233  4568 D GhDiag  : flow_closed dst=fd00:1:…:49104->2001:4860:…:443 reason=upstream_eof up=809 down=0 ms=1345 probe=false
10-26 01:53:40.457  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=422
10-26 01:53:40.734  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:40.817  3233  4639 D GhDiag  : flow_established 10ms
10-26 01:53:41.008  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=529
10-26 01:53:41.148  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=125
10-26 01:53:41.151  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:41.201  3233  4684 D GhDiag  : flow_established 4ms
10-26 01:53:41.270  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=107
10-26 01:53:41.613  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=326
10-26 01:53:41.615  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:41.623  3233  4692 D GhDiag  : flow_established 1ms
10-26 01:53:41.963  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=308
10-26 01:53:42.216  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=242
10-26 01:53:42.221  3233  4527 D GhDiag  : flow_open v4 dst=34.3.x.x:443 probe=false
10-26 01:53:42.262  3233  4716 D GhDiag  : flow_established 24ms
10-26 01:53:42.781  3233  4526 D GhDiag  : stats t=5s packets=109 tcp=69 dns53=12 otherUdp=13 activeTcp=5 flowsOpened=12 flowsEstablished=12 connectFailures=0 retransmits=0 appUp=5132 appDown=31526 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:53:42.819  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=180
10-26 01:53:42.941  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.040  3233  4735 D GhDiag  : flow_established 7ms
10-26 01:53:43.133  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.178  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=313
10-26 01:53:43.210  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:43.231  3233  4746 D GhDiag  : flow_established 30ms
10-26 01:53:43.359  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=170
10-26 01:53:43.442  3233  4750 D GhDiag  : flow_established 162ms
10-26 01:53:43.473  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=111
10-26 01:53:43.506  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.516  3233  4532 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5746 probe=true
10-26 01:53:43.682  3233  4761 D GhDiag  : flow_established 167ms
10-26 01:53:43.737  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.855  3233  4769 D GhDiag  : flow_established 2ms
10-26 01:53:44.075  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:44.097  3233  4772 D GhDiag  : flow_established 12ms
10-26 01:53:44.138  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:44.162  3233  4775 D GhDiag  : flow_established 8ms
10-26 01:53:44.196  3233  4527 D GhDiag  : flow_closed dst=10.8.x.x:56106->172.217.x.x:443 reason=client_rst up=0 down=0 ms=58 probe=false
10-26 01:53:44.917  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.016  3233  4781 D GhDiag  : flow_established 48ms
10-26 01:53:45.294  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.351  3233  4785 D GhDiag  : flow_established 35ms
10-26 01:53:46.585  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.620  3233  4797 D GhDiag  : flow_established 11ms
10-26 01:53:46.674  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.705  3233  4804 D GhDiag  : flow_established 28ms
10-26 01:53:46.747  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:46.899  3233  4807 D GhDiag  : flow_established 107ms
10-26 01:53:47.334  3233  4528 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:53:47.335  3233  4528 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:53:47.345  3233  4551 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:53:47.367  3233  4528 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=473 firstByteMs=544 checksums=0
10-26 01:53:47.517  3233  4810 D GhDiag  : flow_established 23ms
10-26 01:53:47.783  3233  4526 D GhDiag  : stats t=10s packets=792 tcp=743 dns53=12 otherUdp=17 activeTcp=16 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=77448 appDown=1653914 probeUp=182 probeDown=402 probeFlows=1 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:53:48.056  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49718->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6441 probe=false
10-26 01:53:48.162  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49122->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7429 probe=false
10-26 01:53:48.182  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48712->2001:4860:…:443
10-26 01:53:48.226  3233  4551 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:53:48.226  3233  4551 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:53:48.259  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48712->2001:4860:4842:400:::443
10-26 01:53:48.489  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:39774->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7337 probe=false
10-26 01:53:48.518  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:52410->2001:4860:…:443
10-26 01:53:48.519  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:52410->2001:4860:4844:400:::443
10-26 01:53:48.519  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:48.540  3233  4825 D GhDiag  : flow_established 6ms
10-26 01:53:48.545  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50958->2001:4860:…:443
10-26 01:53:48.546  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50958->2001:4860:4847:400:::443
10-26 01:53:49.561  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49734->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6627 probe=false
10-26 01:53:49.670  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:32990->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6537 probe=false
10-26 01:53:50.033  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48678->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6531 probe=false
10-26 01:53:50.388  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48684->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6313 probe=false
10-26 01:53:50.389  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:32992->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6654 probe=false
10-26 01:53:50.603  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=680
10-26 01:53:50.660  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:49748->2001:4860:…:443
10-26 01:53:50.660  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:49748->2001:4860:482d:400:::443
10-26 01:53:50.665  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:52208->2001:4860:…:443
10-26 01:53:50.665  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:52208->2001:4860:4827:400:::443
10-26 01:53:50.668  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48888->2001:4860:…:443
10-26 01:53:50.668  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48888->2001:4860:482c:400:::443
10-26 01:53:50.668  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:47138->2001:4860:…:443
10-26 01:53:50.669  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:47138->2001:4860:4828:400:::443
10-26 01:53:50.672  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:59546->2001:4860:…:443
10-26 01:53:50.672  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:59546->2001:4860:4826:400:::443
10-26 01:53:50.672  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:42162->2001:4860:…:443
10-26 01:53:50.673  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:42162->2001:4860:482a:400:::443
10-26 01:53:50.673  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:42744->2001:4860:…:443
10-26 01:53:50.694  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:42744->2001:4860:482b:400:::443
10-26 01:53:50.695  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:39244->2001:4860:…:443
10-26 01:53:50.695  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:39244->2001:4860:4829:400:::443
10-26 01:53:50.698  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:50.716  3233  4902 D GhDiag  : flow_established 4ms
10-26 01:53:50.746  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=141
10-26 01:53:50.747  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:50.765  3233  4906 D GhDiag  : flow_established 5ms
10-26 01:53:50.808  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=50
10-26 01:53:51.490  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=668
10-26 01:53:51.565  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48688->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6271 probe=false
10-26 01:53:51.819  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:51.900  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=175
10-26 01:53:52.112  3233  4970 D GhDiag  : flow_established 6ms
10-26 01:53:52.430  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=528
10-26 01:53:52.538  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48686->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7620 probe=false
10-26 01:53:52.565  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:52.596  3233  4986 D GhDiag  : flow_established 20ms
10-26 01:53:52.728  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:52.746  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=237
10-26 01:53:52.787  3233  4526 D GhDiag  : stats t=15s packets=1550 tcp=1481 dns53=20 otherUdp=22 activeTcp=12 flowsOpened=31 flowsEstablished=30 connectFailures=0 retransmits=91 appUp=83897 appDown=3186522 probeUp=182 probeDown=804 probeFlows=1 dnsOk=19 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:53:52.890  3233  4992 D GhDiag  : flow_established 69ms
10-26 01:53:52.919  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=166
10-26 01:53:52.973  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:53.063  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=115
10-26 01:53:53.128  3233  5009 D GhDiag  : flow_established 12ms
10-26 01:53:53.221  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=97
10-26 01:53:53.237  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:53.247  3233  5018 D GhDiag  : flow_established 2ms
10-26 01:53:53.256  3233  4532 D GhDiag  : flow_closed dst=10.8.x.x:41002->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5910 probe=true
10-26 01:53:53.267  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48700->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6521 probe=false
10-26 01:53:53.445  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:53.480  3233  5028 D GhDiag  : flow_established 19ms
10-26 01:53:53.713  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=77
10-26 01:53:53.774  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=59
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d7a2c59 u0 com.ghprotocol.app/.MainActivity)/@0x2b1ab0 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{47772b0 u0 com.ghprotocol.app/.MainActivity)/@0x89c2d29 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:53:30.116   824   857 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{d7a2c59 u0 com.ghprotocol.app/.MainActivity)/@0x2b1ab0 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{47772b0 u0 com.ghprotocol.app/.MainActivity)/@0x89c2d29 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:53:30.237   518   590 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{a2722f9 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:53:30.412  1437  1478 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-26 01:53:30.692   518   538 W ActivityTaskManager: Activity pause timeout for ActivityRecord{d7a2c59 u0 com.ghprotocol.app/.MainActivity t8}
10-26 01:53:30.773   824   857 V WindowManagerShell: Transition requested: android.os.BinderProxy@b528fe0 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=59513 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@13db299} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{f05d95e com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:53:30.835  1391  4085 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-26 01:53:31.222   518  2365 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-26 01:53:31.223   518  2365 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-26 01:53:31.223   518  2365 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-26 01:53:32.107   518   535 V WindowManager: Sent Transition #8 createdAt=10-26 01:53:30.154 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=59513 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{d47a86d Task{da1b06b #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{47be543 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:53:33.846  4243  4243 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:53:33.863  4243  4243 I AndroidRuntime: Using default boot image
10-26 01:53:33.863  4243  4243 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:53:34.161  4243  4243 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:53:34.323   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{f91af59 com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:53:34.323   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{c4af71e com.google.android.gm/10141} BLOCKED
10-26 01:53:34.324   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{26a8bff com.google.android.devicelockcontroller/10175} BLOCKED
10-26 01:53:34.324   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{43f7dcc com.google.android.rkpdapp/10180} BLOCKED
10-26 01:53:34.324   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{f24e815 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:53:34.324   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{1412fdd com.google.android.projection.gearhead/10123} BLOCKED
10-26 01:53:35.295  4243  4243 D AndroidRuntime: Shutting down VM
10-26 01:53:36.627   518  2366 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-26 01:53:37.121  3233  3536 W .ghprotocol.app: Verification of void kotlin.io.LinesSequence$iterator$1.<init>(kotlin.io.LinesSequence) took 153.829ms (39.00 bytecodes/s) (1416B approximate peak alloc)
10-26 01:53:37.542   518   896 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-26 01:53:37.655   518   992 I Vpn     : Established by com.ghprotocol.app on tun0
10-26 01:53:37.660  3233  3233 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:53:37.769  3233  4528 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:53:37.776  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:53:37.777  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:53:37.777  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:37.929   518  1928 I ImeTracker: com.ghprotocol.app:3b38e218: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:53:37.929   518  1928 I ImeTracker: com.ghprotocol.app:3b38e218: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:53:37.935  1522  1522 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:53:38.206  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:38.241  3233  4533 D GhDiag  : flow_established 148ms
10-26 01:53:38.321  3233  4527 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:53:38.322  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47058->fd00:1:…:853
10-26 01:53:38.327  3233  4528 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:53:38.340  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47058->fd00:1::1:853
10-26 01:53:38.381  3233  4557 D GhDiag  : flow_established 17ms
10-26 01:53:38.463  3233  4527 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:53:38.470  3233  4527 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:53:38.470  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:53:38.504  3233  4527 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:53:38.505  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47060->fd00:1:…:853
10-26 01:53:38.507  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47060->fd00:1::1:853
10-26 01:53:38.510  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.510  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v4 proto=17 dst=10.0.x.x:53 len=60
10-26 01:53:38.511  3233  4527 D GhDiag  : tun v4 proto=17 dst=10.0.x.x:53 len=60
10-26 01:53:38.532  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.533  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:38.674  3233  4527 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=130
10-26 01:53:38.674  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:53:38.706  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:38.735  3233  4527 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:53:38.736  3233  4562 D GhDiag  : flow_established 5ms
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.743  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.743  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:53:38.754  3233  4527 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=62
10-26 01:53:38.754  3233  4527 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=394
10-26 01:53:38.766  3233  4566 D GhDiag  : flow_established 8ms
10-26 01:53:38.769  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-26 01:53:38.782  3233  4563 D GhDiag  : flow_established 11ms
10-26 01:53:38.784  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:38.788  3233  4527 D GhDiag  : flow_closed dst=10.8.x.x:56226->142.251.x.x:443 reason=client_rst up=0 down=0 ms=110 probe=false
10-26 01:53:38.799  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=869
10-26 01:53:38.804  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=869
10-26 01:53:38.806  3233  4527 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-26 01:53:38.964  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:39.227  3233  3315 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-26 01:53:39.287  3233  4527 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=130
10-26 01:53:39.296  3233  4527 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:53:39.331  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:47072->fd00:1:…:853
10-26 01:53:39.333  3233  4571 D GhDiag  : flow_established 223ms
10-26 01:53:39.365  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:47072->fd00:1::1:853
10-26 01:53:39.365  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:39.486  3233  4598 D GhDiag  : flow_established 13ms
10-26 01:53:39.640  3233  4527 D GhDiag  : flow_closed dst=fd00:1:…:49108->2001:4860:…:443 reason=client_rst up=0 down=0 ms=827 probe=false
10-26 01:53:39.685  3233  4527 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:59616->10.8.x.x:853
10-26 01:53:39.697  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:59616->10.8.0.1:853
10-26 01:53:39.750  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:39.773  3233  4527 D GhDiag  : flow_closed dst=fd00:1:…:49114->2001:4860:…:443 reason=client_rst up=0 down=0 ms=408 probe=false
10-26 01:53:39.863  3233  4559 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:53:39.864  3233  4559 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1536 probe=false
10-26 01:53:39.926  3233  4608 D GhDiag  : flow_established 2ms
10-26 01:53:40.034  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=1488
10-26 01:53:40.088  3233  4565 D GhDiag  : flow_closed dst=fd00:1:…:58298->2001:4860:…:443 reason=upstream_eof up=809 down=0 ms=1555 probe=false
10-26 01:53:40.089  3233  4568 D GhDiag  : flow_closed dst=fd00:1:…:49104->2001:4860:…:443 reason=upstream_eof up=809 down=0 ms=1345 probe=false
10-26 01:53:40.457  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=422
10-26 01:53:40.734  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:40.754  3233  3316 I .ghprotocol.app: Background young concurrent copying GC freed 89156(4380KB) AllocSpace objects, 2(40KB) LOS objects, 32% free, 8355KB/12MB, paused 84us,54us total 473.942ms
10-26 01:53:40.817  3233  4639 D GhDiag  : flow_established 10ms
10-26 01:53:41.008  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=529
10-26 01:53:41.148  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=125
10-26 01:53:41.151  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:41.201  3233  4684 D GhDiag  : flow_established 4ms
10-26 01:53:41.270  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=107
10-26 01:53:41.613  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=326
10-26 01:53:41.615  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:41.623  3233  4692 D GhDiag  : flow_established 1ms
10-26 01:53:41.963  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=308
10-26 01:53:42.195  3233  3316 I .ghprotocol.app: Background concurrent copying GC freed 57539(4208KB) AllocSpace objects, 15(300KB) LOS objects, 49% free, 8555KB/16MB, paused 36us,14us total 461.409ms
10-26 01:53:42.216  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=242
10-26 01:53:42.221  3233  4527 D GhDiag  : flow_open v4 dst=34.3.x.x:443 probe=false
10-26 01:53:42.262  3233  4716 D GhDiag  : flow_established 24ms
10-26 01:53:42.781  3233  4526 D GhDiag  : stats t=5s packets=109 tcp=69 dns53=12 otherUdp=13 activeTcp=5 flowsOpened=12 flowsEstablished=12 connectFailures=0 retransmits=0 appUp=5132 appDown=31526 probeUp=91 probeDown=402 probeFlows=1 dnsOk=8 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:53:42.819  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=180
10-26 01:53:42.941  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.040  3233  4735 D GhDiag  : flow_established 7ms
10-26 01:53:43.133  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.178  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=313
10-26 01:53:43.210  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:43.231  3233  4746 D GhDiag  : flow_established 30ms
10-26 01:53:43.359  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=170
10-26 01:53:43.442  3233  4750 D GhDiag  : flow_established 162ms
10-26 01:53:43.473  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=111
10-26 01:53:43.506  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.516  3233  4532 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5746 probe=true
10-26 01:53:43.682  3233  4761 D GhDiag  : flow_established 167ms
10-26 01:53:43.704   518  2368 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4764, uid=2000 that is not exported from uid 10192
10-26 01:53:43.737  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:43.855  3233  4769 D GhDiag  : flow_established 2ms
10-26 01:53:44.075  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:44.097  3233  4772 D GhDiag  : flow_established 12ms
10-26 01:53:44.138  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:44.162  3233  4775 D GhDiag  : flow_established 8ms
10-26 01:53:44.196  3233  4527 D GhDiag  : flow_closed dst=10.8.x.x:56106->172.217.x.x:443 reason=client_rst up=0 down=0 ms=58 probe=false
10-26 01:53:44.532   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{fdc78d0 com.google.android.apps.messaging/10130} BLOCKED
10-26 01:53:44.532   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{e8f00c9 com.google.android.gm/10141} BLOCKED
10-26 01:53:44.532   518   569 I AppsFilter: interaction: PackageSetting{4f71993 com.ghprotocol.app/10192} -> PackageSetting{996c3ce com.google.android.contacts/10155} BLOCKED
10-26 01:53:44.917  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.016  3233  4781 D GhDiag  : flow_established 48ms
10-26 01:53:45.294  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:45.351  3233  4785 D GhDiag  : flow_established 35ms
10-26 01:53:45.484  3233  3316 I .ghprotocol.app: Background young concurrent copying GC freed 105770(8145KB) AllocSpace objects, 0(0B) LOS objects, 32% free, 11MB/16MB, paused 292us,814us total 690.603ms
10-26 01:53:46.585  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.620  3233  4797 D GhDiag  : flow_established 11ms
10-26 01:53:46.674  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:46.705  3233  4804 D GhDiag  : flow_established 28ms
10-26 01:53:46.747  3233  4527 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:53:46.899  3233  4807 D GhDiag  : flow_established 107ms
10-26 01:53:47.334  3233  4528 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:53:47.335  3233  4528 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:53:47.345  3233  4551 W .ghprotocol.app: Long monitor contention with owner gh-selftest (4528) at com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int)(TunnelSelfTest.kt:84) waiters=0 in com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int) for 8.955s
10-26 01:53:47.345  3233  4551 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:53:47.367  3233  4528 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=473 firstByteMs=544 checksums=0
10-26 01:53:47.517  3233  4810 D GhDiag  : flow_established 23ms
10-26 01:53:47.549  3233  3316 I .ghprotocol.app: Background concurrent copying GC freed 101236(9152KB) AllocSpace objects, 48(960KB) LOS objects, 49% free, 8360KB/16MB, paused 56us,3.798ms total 874.488ms
10-26 01:53:47.783  3233  4526 D GhDiag  : stats t=10s packets=792 tcp=743 dns53=12 otherUdp=17 activeTcp=16 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=77448 appDown=1653914 probeUp=182 probeDown=402 probeFlows=1 dnsOk=12 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:53:48.056  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49718->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6441 probe=false
10-26 01:53:48.162  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49122->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7429 probe=false
10-26 01:53:48.182  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48712->2001:4860:…:443
10-26 01:53:48.226  3233  4551 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:53:48.226  3233  4551 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:53:48.259  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48712->2001:4860:4842:400:::443
10-26 01:53:48.489  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:39774->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7337 probe=false
10-26 01:53:48.518  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:52410->2001:4860:…:443
10-26 01:53:48.519  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:52410->2001:4860:4844:400:::443
10-26 01:53:48.519  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:48.540  3233  4825 D GhDiag  : flow_established 6ms
10-26 01:53:48.545  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50958->2001:4860:…:443
10-26 01:53:48.546  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50958->2001:4860:4847:400:::443
10-26 01:53:49.551  3233  4532 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-37872 (4718) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:481) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.tick() for 215ms
10-26 01:53:49.561  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:49734->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6627 probe=false
10-26 01:53:49.670  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:32990->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6537 probe=false
10-26 01:53:49.905  3233  3316 W .ghprotocol.app: Suspending all threads took: 18.747ms
10-26 01:53:49.909  3233  3316 I .ghprotocol.app: Background young concurrent copying GC freed 88625(8436KB) AllocSpace objects, 0(0B) LOS objects, 37% free, 10MB/16MB, paused 214us,18.816ms total 964.088ms
10-26 01:53:50.033  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48678->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6531 probe=false
10-26 01:53:50.283  3233  4532 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-37872 (4718) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:481) waiters=1 in void com.ghprotocol.app.core.net.TcpRelay.tick() for 250ms
10-26 01:53:50.388  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48684->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6313 probe=false
10-26 01:53:50.389  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:32992->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6654 probe=false
10-26 01:53:50.514   518   535 V WindowManager:     info={id=10 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{9727f87 Task{6c1be16 #9 type=standard A=10149:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0xee46d8f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{d47a86d Task{da1b06b #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0x9c0c160 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:53:50.603  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=680
10-26 01:53:50.660  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:49748->2001:4860:…:443
10-26 01:53:50.660  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:49748->2001:4860:482d:400:::443
10-26 01:53:50.665  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:52208->2001:4860:…:443
10-26 01:53:50.665  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:52208->2001:4860:4827:400:::443
10-26 01:53:50.668  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48888->2001:4860:…:443
10-26 01:53:50.668  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48888->2001:4860:482c:400:::443
10-26 01:53:50.668  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:47138->2001:4860:…:443
10-26 01:53:50.669  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:47138->2001:4860:4828:400:::443
10-26 01:53:50.672  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:59546->2001:4860:…:443
10-26 01:53:50.672  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:59546->2001:4860:4826:400:::443
10-26 01:53:50.672  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:42162->2001:4860:…:443
10-26 01:53:50.673  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:42162->2001:4860:482a:400:::443
10-26 01:53:50.673  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:42744->2001:4860:…:443
10-26 01:53:50.694  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:42744->2001:4860:482b:400:::443
10-26 01:53:50.695  3233  4527 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:39244->2001:4860:…:443
10-26 01:53:50.695  3233  4527 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:39244->2001:4860:4829:400:::443
10-26 01:53:50.698  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:50.716  3233  4902 D GhDiag  : flow_established 4ms
10-26 01:53:50.746  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=141
10-26 01:53:50.747  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:50.765  3233  4906 D GhDiag  : flow_established 5ms
10-26 01:53:50.808  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=50
10-26 01:53:51.456  3233  4718 W .ghprotocol.app: Long monitor contention with owner gh-tun-read (4527) at void com.ghprotocol.app.core.net.TcpRelay.onPacket(byte[])(TcpRelay.kt:263) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.waitForAckSpace(com.ghprotocol.app.core.net.TcpRelay$Flow) for 114ms
10-26 01:53:51.490  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=668
10-26 01:53:51.565  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48688->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6271 probe=false
10-26 01:53:51.819  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:51.900  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=175
10-26 01:53:52.078  3233  4532 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-37872 (4718) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:481) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.tick() for 290ms
10-26 01:53:52.112  3233  4970 D GhDiag  : flow_established 6ms
10-26 01:53:52.430  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=528
10-26 01:53:52.538  3233  4532 D GhDiag  : flow_closed dst=fd00:1:…:48686->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7620 probe=false
10-26 01:53:52.565  3233  4527 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:53:52.595  3233  3316 I .ghprotocol.app: Background concurrent copying GC freed 111727(9945KB) AllocSpace objects, 4(80KB) LOS objects, 49% free, 8723KB/17MB, paused 3.259ms,22us total 1.392s
10-26 01:53:52.596  3233  4986 D GhDiag  : flow_established 20ms
10-26 01:53:52.728  3233  4527 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:53:52.746  3233  4561 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=237
10-26 01:53:52.787  3233  4526 D GhDiag  : stats t=15s packets=1550 tcp=1481 dns53=20 otherUdp=22 activeTcp=12 flowsOpened=31 flowsEstablished=30 connectFailures=0 retransmits=91 appUp=83897 appDown=3186522 probeUp=182 probeDown=804 probeFlows=1 dnsOk=19 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:53:52.890  3233  4992 D GhDiag  : flow_established 69ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
