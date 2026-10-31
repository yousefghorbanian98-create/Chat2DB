## gh-protocol E2E log — 2026-10-31T09:00:42Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-31T08:58:28Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 31 08:56 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 31 08:59 .
drwxr-xr-x 3 runner runner 4096 Oct 31 08:59 ..
drwxr-xr-x 3 runner runner 4096 Oct 31 08:59 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 31 08:59 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.13.0 (build_id 16740729) (CL:N/A)
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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15983 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15983 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 2993
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
INFO         |   androidboot.serialno=EMULATOR37X2X13X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7f7b5fa01000 as it is in the protected range from 0x7f7a5fa00000 to 0x7f7b5fc00000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 39400 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 116
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 2993) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms

### gradle-build.log (tail)
To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues FROM-CACHE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources FROM-CACHE
> Task :app:extractDeepLinksDebug FROM-CACHE
> Task :app:packageDebugResources FROM-CACHE
> Task :app:parseDebugLocalResources FROM-CACHE
> Task :app:mapDebugSourceSetPaths
> Task :app:javaPreCompileDebug FROM-CACHE
> Task :app:checkDebugAarMetadata
> Task :app:desugarDebugFileDependencies FROM-CACHE
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:mergeDebugResources FROM-CACHE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets FROM-CACHE
> Task :app:mergeLibDexDebug FROM-CACHE
> Task :app:mergeDebugJniLibFolders
> Task :app:processDebugManifestForPackage
> Task :app:mergeExtDexDebug FROM-CACHE
> Task :app:writeDebugAppMetadata
> Task :app:mergeDebugNativeLibs
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:processDebugResources

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:608:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics FROM-CACHE
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1793437054330.json

BUILD SUCCESSFUL in 59s
37 actionable tasks: 25 executed, 12 from cache
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
app up (try 1, pid 3254)
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
    inet6 fe80::b26f:4617:a04a:df10/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.4): 56(84) bytes.

--- 140.82.113.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
relay self-test PASS (real remote payload through the relay)
10-31 09:00:36.063  3254  4486 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 09:00:36.070  3254  4486 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=197 firstByteMs=301 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-31 09:00:32.336  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=334
10-31 09:00:32.395  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.503  3254  4713 D GhDiag  : flow_established 10ms
10-31 09:00:32.540  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=94
10-31 09:00:32.694  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.761  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.778  3254  4716 D GhDiag  : flow_established 16ms
10-31 09:00:32.835  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.846  3254  4719 D GhDiag  : flow_established 56ms
10-31 09:00:32.919  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=364
10-31 09:00:33.096  3254  4721 D GhDiag  : flow_established 96ms
10-31 09:00:34.347  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.351  3254  4742 D GhDiag  : flow_established 3ms
10-31 09:00:34.669  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:34.684  3254  4752 D GhDiag  : flow_established 6ms
10-31 09:00:34.791  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=285
10-31 09:00:34.890  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=97
10-31 09:00:34.922  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.965  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:35.039  3254  4756 D GhDiag  : flow_established 26ms
10-31 09:00:35.042  3254  4757 D GhDiag  : flow_established 26ms
10-31 09:00:36.063  3254  4486 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-31 09:00:36.063  3254  4486 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 09:00:36.070  3254  4486 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=197 firstByteMs=301 checksums=0
10-31 09:00:36.198  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=166
10-31 09:00:36.543  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=331
10-31 09:00:36.578  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:36.689  3254  4831 D GhDiag  : flow_established 57ms
10-31 09:00:36.781  3254  4484 D GhDiag  : stats t=10s packets=216 tcp=166 dns53=20 otherUdp=10 activeTcp=17 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=61156 appDown=27482 probeUp=91 probeDown=402 probeFlows=0 dnsOk=18 dnsFail=0 state=VERIFIED ipv6=route_only
10-31 09:00:37.020  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=476
10-31 09:00:37.163  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55398->2001:4860:…:443
10-31 09:00:37.181  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55398->2001:4860:4841:400:::443
10-31 09:00:37.182  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45964->2001:4860:…:443
10-31 09:00:37.183  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45964->2001:4860:4846:400:::443
10-31 09:00:37.183  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36924->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36924->2001:4860:4843:400:::443
10-31 09:00:37.184  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37054->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37054->2001:4860:4840:400:::443
10-31 09:00:37.201  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:46696->2001:4860:…:443
10-31 09:00:37.201  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:46696->2001:4860:4844:400:::443
10-31 09:00:37.202  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41824->2001:4860:…:443
10-31 09:00:37.202  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:41824->2001:4860:4845:400:::443
10-31 09:00:37.204  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:54288->2001:4860:…:443
10-31 09:00:37.204  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:54288->2001:4860:4847:400:::443
10-31 09:00:37.221  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:53836->2001:4860:…:443
10-31 09:00:37.221  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:53836->2001:4860:4842:400:::443
10-31 09:00:37.231  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:37.282  3254  4860 D GhDiag  : flow_established 23ms
10-31 09:00:37.425  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=395
10-31 09:00:37.592  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=61156 bytes
10-31 09:00:36.781  3254  4484 D GhDiag  : stats t=10s packets=216 tcp=166 dns53=20 otherUdp=10 activeTcp=17 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=61156 appDown=27482 probeUp=91 probeDown=402 probeFlows=0 dnsOk=18 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-31 09:00:36.063  3254  4486 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-31 09:00:17.562  3254  3254 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-31 09:00:17.568  3254  3254 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-31 09:00:17.935  3254  3254 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-31 09:00:18.088  3254  3254 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 09:00:18.088  3254  3254 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 09:00:18.088  3254  3254 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-31 09:00:18.247  3254  3254 D GhDiag  : connect: core.start=true 
10-31 09:00:26.733  3254  3254 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-31 09:00:26.759  3254  4486 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 09:00:26.761  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 09:00:26.761  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-31 09:00:26.762  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:26.950  3254  4489 D GhDiag  : flow_established 59ms
10-31 09:00:27.060  3254  4486 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-31 09:00:27.081  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=112
10-31 09:00:27.082  3254  4506 D GhDiag  : flow_established 4ms
10-31 09:00:27.088  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 09:00:27.088  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 09:00:27.092  3254  4485 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 09:00:27.093  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:39502->fd00:1:…:853
10-31 09:00:27.097  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:39502->fd00:1::1:853
10-31 09:00:27.111  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-31 09:00:27.112  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-31 09:00:27.132  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-31 09:00:27.140  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-31 09:00:27.141  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 09:00:27.150  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 09:00:27.153  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:27.303  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=179
10-31 09:00:27.304  3254  4514 D GhDiag  : dns_reply 193ms path=doh:cloudflare-dns.com bytes=61
10-31 09:00:27.466  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=162
10-31 09:00:27.477  3254  4514 D GhDiag  : dns_reply 365ms path=doh:cloudflare-dns.com bytes=49
10-31 09:00:27.557  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=60
10-31 09:00:27.567  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:27.571  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=60
10-31 09:00:27.679  3254  4485 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-31 09:00:27.698  3254  4485 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 09:00:27.734  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.735  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=557
10-31 09:00:27.736  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:27.736  3254  4527 D GhDiag  : flow_established 130ms
10-31 09:00:27.736  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=242
10-31 09:00:27.740  3254  4514 D GhDiag  : dns_reply 608ms path=doh:cloudflare-dns.com bytes=177
10-31 09:00:27.778  3254  4485 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 09:00:27.780  3254  4485 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 09:00:27.817  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.820  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-31 09:00:27.830  3254  4529 D GhDiag  : flow_established 40ms
10-31 09:00:27.831  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=40
10-31 09:00:27.831  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=297
10-31 09:00:27.929  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=40
10-31 09:00:27.977  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=214
10-31 09:00:27.979  3254  4514 D GhDiag  : dns_reply 838ms path=doh:cloudflare-dns.com bytes=273
10-31 09:00:27.988  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:57822->10.8.x.x:853
10-31 09:00:27.989  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:57822->10.8.0.1:853
10-31 09:00:28.023  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:39518->fd00:1:…:853
10-31 09:00:28.027  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:39518->fd00:1::1:853
10-31 09:00:28.027  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:38162->10.8.x.x:853
10-31 09:00:28.027  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:38162->10.8.0.1:853
10-31 09:00:28.089  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:28.119  3254  4509 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-31 09:00:28.122  3254  4509 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1062 probe=false
10-31 09:00:28.199  3254  4543 D GhDiag  : flow_established 6ms
10-31 09:00:28.332  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=352
10-31 09:00:28.537  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=201
10-31 09:00:28.687  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=128
10-31 09:00:28.999  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=306
10-31 09:00:29.013  3254  4485 D GhDiag  : flow_open v4 dst=34.3.x.x:443 probe=false
10-31 09:00:29.017  3254  4569 D GhDiag  : flow_established 4ms
10-31 09:00:30.139  3254  4485 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-31 09:00:30.163  3254  4639 D GhDiag  : flow_established 4ms
10-31 09:00:30.666  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=427
10-31 09:00:31.309  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=552
10-31 09:00:31.323  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.482  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.486  3254  4670 D GhDiag  : flow_established 118ms
10-31 09:00:31.593  3254  4672 D GhDiag  : flow_established 21ms
10-31 09:00:31.710  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.732  3254  4679 D GhDiag  : flow_established 5ms
10-31 09:00:31.781  3254  4484 D GhDiag  : stats t=5s packets=136 tcp=104 dns53=10 otherUdp=7 activeTcp=8 flowsOpened=10 flowsEstablished=10 connectFailures=0 retransmits=0 appUp=53182 appDown=26146 probeUp=91 probeDown=402 probeFlows=1 dnsOk=10 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 09:00:31.982  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=127
10-31 09:00:32.148  3254  4488 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5389 probe=true
10-31 09:00:32.336  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=334
10-31 09:00:32.395  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.503  3254  4713 D GhDiag  : flow_established 10ms
10-31 09:00:32.540  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=94
10-31 09:00:32.694  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.761  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.778  3254  4716 D GhDiag  : flow_established 16ms
10-31 09:00:32.835  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.846  3254  4719 D GhDiag  : flow_established 56ms
10-31 09:00:32.919  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=364
10-31 09:00:33.096  3254  4721 D GhDiag  : flow_established 96ms
10-31 09:00:34.347  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.351  3254  4742 D GhDiag  : flow_established 3ms
10-31 09:00:34.669  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:34.684  3254  4752 D GhDiag  : flow_established 6ms
10-31 09:00:34.791  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=285
10-31 09:00:34.890  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=97
10-31 09:00:34.922  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.965  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:35.039  3254  4756 D GhDiag  : flow_established 26ms
10-31 09:00:35.042  3254  4757 D GhDiag  : flow_established 26ms
10-31 09:00:36.063  3254  4486 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-31 09:00:36.063  3254  4486 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 09:00:36.070  3254  4486 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=197 firstByteMs=301 checksums=0
10-31 09:00:36.198  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=166
10-31 09:00:36.543  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=331
10-31 09:00:36.578  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:36.689  3254  4831 D GhDiag  : flow_established 57ms
10-31 09:00:36.781  3254  4484 D GhDiag  : stats t=10s packets=216 tcp=166 dns53=20 otherUdp=10 activeTcp=17 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=61156 appDown=27482 probeUp=91 probeDown=402 probeFlows=0 dnsOk=18 dnsFail=0 state=VERIFIED ipv6=route_only
10-31 09:00:37.020  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=476
10-31 09:00:37.163  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55398->2001:4860:…:443
10-31 09:00:37.181  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55398->2001:4860:4841:400:::443
10-31 09:00:37.182  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45964->2001:4860:…:443
10-31 09:00:37.183  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45964->2001:4860:4846:400:::443
10-31 09:00:37.183  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36924->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36924->2001:4860:4843:400:::443
10-31 09:00:37.184  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37054->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37054->2001:4860:4840:400:::443
10-31 09:00:37.201  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:46696->2001:4860:…:443
10-31 09:00:37.201  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:46696->2001:4860:4844:400:::443
10-31 09:00:37.202  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41824->2001:4860:…:443
10-31 09:00:37.202  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:41824->2001:4860:4845:400:::443
10-31 09:00:37.204  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:54288->2001:4860:…:443
10-31 09:00:37.204  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:54288->2001:4860:4847:400:::443
10-31 09:00:37.221  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:53836->2001:4860:…:443
10-31 09:00:37.221  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:53836->2001:4860:4842:400:::443
10-31 09:00:37.231  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:37.282  3254  4860 D GhDiag  : flow_established 23ms
10-31 09:00:37.425  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=395
10-31 09:00:37.592  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 09:00:37.694  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55366->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6371 probe=false
10-31 09:00:37.723  3254  4863 D GhDiag  : flow_established 108ms
10-31 09:00:37.864  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55386->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6154 probe=false
10-31 09:00:37.864  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55380->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6382 probe=false
10-31 09:00:37.920  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 09:00:38.087  3254  4874 D GhDiag  : flow_established 161ms
10-31 09:00:38.975  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55392->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6213 probe=false
10-31 09:00:39.335  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55394->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6500 probe=false
10-31 09:00:39.737  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:44304->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=7328 probe=false
10-31 09:00:39.940  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55390->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7245 probe=false
10-31 09:00:40.990  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:39362->2001:4860:…:443
10-31 09:00:40.991  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:39362->2001:4860:482d:400:::443
10-31 09:00:40.992  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:40758->2001:4860:…:443
10-31 09:00:40.994  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:40758->2001:4860:482a:400:::443
10-31 09:00:40.995  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:52752->2001:4860:…:443
10-31 09:00:40.995  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:52752->2001:4860:4826:400:::443
10-31 09:00:40.996  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36116->2001:4860:…:443
10-31 09:00:40.996  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36116->2001:4860:482b:400:::443
10-31 09:00:40.998  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:46664->2001:4860:…:443
10-31 09:00:40.998  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:46664->2001:4860:4827:400:::443
10-31 09:00:40.999  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:40258->2001:4860:…:443
10-31 09:00:40.999  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:40258->2001:4860:482c:400:::443
10-31 09:00:41.001  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50880->2001:4860:…:443
10-31 09:00:41.002  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50880->2001:4860:4829:400:::443
10-31 09:00:41.002  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48930->2001:4860:…:443
10-31 09:00:41.002  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48930->2001:4860:4828:400:::443
10-31 09:00:41.003  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 09:00:41.017  3254  4957 D GhDiag  : flow_established 3ms
10-31 09:00:41.101  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=572
10-31 09:00:41.261  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=159
10-31 09:00:41.288  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 09:00:18.088  3254  3254 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 09:00:18.088  3254  3254 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-31 09:00:18.247  3254  3254 D GhDiag  : connect: core.start=true 
10-31 09:00:18.963  3991  3991 D AndroidRuntime: Shutting down VM
10-31 09:00:19.005   519   918 D CoreBackPreview: Window{3b5b476 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@a3cd7fa, mPriority=0, mIsAnimationCallback=false}
10-31 09:00:19.800  4074  4074 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=54865 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-31 09:00:20.626  4278  4278 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-31 09:00:20.629  4278  4278 I AndroidRuntime: Using default boot image
10-31 09:00:20.629  4278  4278 I AndroidRuntime: Leaving lock profiling enabled
10-31 09:00:20.794  4278  4278 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-31 09:00:20.905   834   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@fe86bfe: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity)/@0xad0a75 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{629e6e4 u0 com.ghprotocol.app/.MainActivity)/@0xe5b4a0a sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 09:00:20.906   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s639ms
10-31 09:00:20.921   834   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity)/@0xad0a75 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{629e6e4 u0 com.ghprotocol.app/.MainActivity)/@0xe5b4a0a sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 09:00:20.921   834   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity)/@0xad0a75 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{629e6e4 u0 com.ghprotocol.app/.MainActivity)/@0xe5b4a0a sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 09:00:20.933   519   536 V WindowManager: Sent Transition #7 createdAt=10-31 09:00:17.267 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=57778 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{dbc16e2 Task{8a32eac #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{40f0779 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-31 09:00:20.933   519   536 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity)/@0x68abdc5 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{629e6e4 u0 com.ghprotocol.app/.MainActivity)/@0x6c55c3c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 09:00:21.300   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@86249ba TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=61743 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@42c406b} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{3a37c8 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-31 09:00:21.753   519   539 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity t8}
10-31 09:00:21.754   519   539 W ActivityTaskManager: Activity pause timeout for ActivityRecord{4d7c408 u0 com.ghprotocol.app/.MainActivity t8}
10-31 09:00:21.851  3254  3322 I .ghprotocol.app: Background concurrent copying GC freed 101459(5300KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6551KB/12MB, paused 32us,23us total 1.865s
10-31 09:00:22.021   519   904 I ImeTracker: com.ghprotocol.app:6f6c9307: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-31 09:00:22.022   519   904 I ImeTracker: com.ghprotocol.app:6f6c9307: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-31 09:00:22.068  1560  1560 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-31 09:00:22.597   519  2554 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-31 09:00:22.599   519  2554 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-31 09:00:22.599   519  2554 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-31 09:00:23.729   519   536 V WindowManager: Sent Transition #8 createdAt=10-31 09:00:21.241 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=61743 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{dbc16e2 Task{8a32eac #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5f99e51 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-31 09:00:24.613   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{c2ca70f com.google.android.googlequicksearchbox/10132} BLOCKED
10-31 09:00:24.614   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{e83e39c com.google.android.apps.messaging/10129} BLOCKED
10-31 09:00:24.614   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{429a1a5 com.google.android.gm/10144} BLOCKED
10-31 09:00:24.614   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{f98497a com.google.android.rkpdapp/10179} BLOCKED
10-31 09:00:24.614   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{9707b46 com.google.android.projection.gearhead/10123} BLOCKED
10-31 09:00:24.800  4278  4278 D AndroidRuntime: Shutting down VM
10-31 09:00:26.033   519   918 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-31 09:00:26.564  1660  1660 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-31 09:00:26.713   519  1810 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-31 09:00:26.731   519  1935 I Vpn     : Established by com.ghprotocol.app on tun0
10-31 09:00:26.733  3254  3254 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-31 09:00:26.759  3254  4486 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 09:00:26.761  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 09:00:26.761  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-31 09:00:26.762  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:26.890   519  1935 I ImeTracker: com.ghprotocol.app:5bc073: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-31 09:00:26.890   519  1935 I ImeTracker: com.ghprotocol.app:5bc073: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-31 09:00:26.895  1560  1560 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-31 09:00:26.950  3254  4489 D GhDiag  : flow_established 59ms
10-31 09:00:27.060  3254  4486 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-31 09:00:27.081  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=112
10-31 09:00:27.082  3254  4506 D GhDiag  : flow_established 4ms
10-31 09:00:27.088  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 09:00:27.088  3254  4485 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 09:00:27.092  3254  4485 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 09:00:27.093  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:39502->fd00:1:…:853
10-31 09:00:27.097  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:39502->fd00:1::1:853
10-31 09:00:27.111  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-31 09:00:27.112  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=61
10-31 09:00:27.132  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-31 09:00:27.140  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=77
10-31 09:00:27.141  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 09:00:27.150  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 09:00:27.153  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:27.214  1660  1660 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-31 09:00:27.270  1660  2519 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-31 09:00:27.270  1660  2519 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-31 09:00:27.303  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=179
10-31 09:00:27.304  3254  4514 D GhDiag  : dns_reply 193ms path=doh:cloudflare-dns.com bytes=61
10-31 09:00:27.466  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=162
10-31 09:00:27.477  3254  4514 D GhDiag  : dns_reply 365ms path=doh:cloudflare-dns.com bytes=49
10-31 09:00:27.557  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=60
10-31 09:00:27.567  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:27.571  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=60
10-31 09:00:27.679  3254  4485 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-31 09:00:27.698  3254  4485 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 09:00:27.734  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.735  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=557
10-31 09:00:27.736  3254  4485 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 09:00:27.736  3254  4527 D GhDiag  : flow_established 130ms
10-31 09:00:27.736  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=242
10-31 09:00:27.740  3254  4514 D GhDiag  : dns_reply 608ms path=doh:cloudflare-dns.com bytes=177
10-31 09:00:27.778  3254  4485 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 09:00:27.780  3254  4485 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 09:00:27.817  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.820  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=6 dst=172.217.x.x:443 len=40
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-31 09:00:27.823  3254  4485 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=68
10-31 09:00:27.830  3254  4529 D GhDiag  : flow_established 40ms
10-31 09:00:27.831  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=40
10-31 09:00:27.831  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=297
10-31 09:00:27.929  3254  4485 D GhDiag  : tun v4 proto=6 dst=192.178.x.x:443 len=40
10-31 09:00:27.977  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=214
10-31 09:00:27.979  3254  4514 D GhDiag  : dns_reply 838ms path=doh:cloudflare-dns.com bytes=273
10-31 09:00:27.988  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:57822->10.8.x.x:853
10-31 09:00:27.989  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:57822->10.8.0.1:853
10-31 09:00:28.023  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:39518->fd00:1:…:853
10-31 09:00:28.027  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:39518->fd00:1::1:853
10-31 09:00:28.027  3254  4485 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:38162->10.8.x.x:853
10-31 09:00:28.027  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:38162->10.8.0.1:853
10-31 09:00:28.089  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:28.093  3254  3321 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-31 09:00:28.119  3254  4509 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-31 09:00:28.122  3254  4509 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1062 probe=false
10-31 09:00:28.199  3254  4543 D GhDiag  : flow_established 6ms
10-31 09:00:28.332  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=352
10-31 09:00:28.537  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=201
10-31 09:00:28.687  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=128
10-31 09:00:28.999  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=306
10-31 09:00:29.013  3254  4485 D GhDiag  : flow_open v4 dst=34.3.x.x:443 probe=false
10-31 09:00:29.017  3254  4569 D GhDiag  : flow_established 4ms
10-31 09:00:29.816  3254  3322 W .ghprotocol.app: Suspending all threads took: 8.655ms
10-31 09:00:29.818  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 66215(4915KB) AllocSpace objects, 0(0B) LOS objects, 34% free, 8648KB/12MB, paused 801us,8.714ms total 616.737ms
10-31 09:00:30.039  1457  3221 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-31 09:00:30.114  1419  4108 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-31 09:00:30.139  3254  4485 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-31 09:00:30.163  3254  4639 D GhDiag  : flow_established 4ms
10-31 09:00:30.666  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=427
10-31 09:00:31.083  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 61348(5145KB) AllocSpace objects, 0(0B) LOS objects, 35% free, 8406KB/12MB, paused 44us,14us total 120.782ms
10-31 09:00:31.309  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=552
10-31 09:00:31.323  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.482  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.486  3254  4670 D GhDiag  : flow_established 118ms
10-31 09:00:31.593  3254  4672 D GhDiag  : flow_established 21ms
10-31 09:00:31.710  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:31.732  3254  4679 D GhDiag  : flow_established 5ms
10-31 09:00:31.781  3254  4484 D GhDiag  : stats t=5s packets=136 tcp=104 dns53=10 otherUdp=7 activeTcp=8 flowsOpened=10 flowsEstablished=10 connectFailures=0 retransmits=0 appUp=53182 appDown=26146 probeUp=91 probeDown=402 probeFlows=1 dnsOk=10 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 09:00:31.982  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=127
10-31 09:00:32.148  3254  4488 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5389 probe=true
10-31 09:00:32.209   519  2228 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4705, uid=2000 that is not exported from uid 10192
10-31 09:00:32.312  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 52522(4492KB) AllocSpace objects, 0(0B) LOS objects, 27% free, 9511KB/12MB, paused 3.908ms,122us total 502.625ms
10-31 09:00:32.336  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=334
10-31 09:00:32.395  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.503  3254  4713 D GhDiag  : flow_established 10ms
10-31 09:00:32.540  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=94
10-31 09:00:32.694  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.761  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.778  3254  4716 D GhDiag  : flow_established 16ms
10-31 09:00:32.835  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:32.846  3254  4719 D GhDiag  : flow_established 56ms
10-31 09:00:32.919  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=364
10-31 09:00:33.096  3254  4721 D GhDiag  : flow_established 96ms
10-31 09:00:34.347  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.351  3254  4742 D GhDiag  : flow_established 3ms
10-31 09:00:34.669  3254  4485 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 09:00:34.684  3254  4752 D GhDiag  : flow_established 6ms
10-31 09:00:34.791  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=285
10-31 09:00:34.890  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=97
10-31 09:00:34.922  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:34.965  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:35.039  3254  4756 D GhDiag  : flow_established 26ms
10-31 09:00:35.042  3254  4757 D GhDiag  : flow_established 26ms
10-31 09:00:35.390  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 54137(4328KB) AllocSpace objects, 0(0B) LOS objects, 21% free, 10MB/12MB, paused 319us,15us total 128.247ms
10-31 09:00:35.925   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{e2ec803 com.google.android.apps.messaging/10129} BLOCKED
10-31 09:00:35.925   519   570 I AppsFilter: interaction: PackageSetting{1639f8d com.ghprotocol.app/10192} -> PackageSetting{2e4380 com.google.android.contacts/10153} BLOCKED
10-31 09:00:36.063  3254  4486 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-31 09:00:36.063  3254  4486 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 09:00:36.070  3254  4486 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=197 firstByteMs=301 checksums=0
10-31 09:00:36.198  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=166
10-31 09:00:36.543  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=331
10-31 09:00:36.578  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:36.689  3254  4831 D GhDiag  : flow_established 57ms
10-31 09:00:36.781  3254  4484 D GhDiag  : stats t=10s packets=216 tcp=166 dns53=20 otherUdp=10 activeTcp=17 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=61156 appDown=27482 probeUp=91 probeDown=402 probeFlows=0 dnsOk=18 dnsFail=0 state=VERIFIED ipv6=route_only
10-31 09:00:37.020  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=476
10-31 09:00:37.163  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55398->2001:4860:…:443
10-31 09:00:37.181  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55398->2001:4860:4841:400:::443
10-31 09:00:37.182  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45964->2001:4860:…:443
10-31 09:00:37.183  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45964->2001:4860:4846:400:::443
10-31 09:00:37.183  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36924->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36924->2001:4860:4843:400:::443
10-31 09:00:37.184  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37054->2001:4860:…:443
10-31 09:00:37.184  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37054->2001:4860:4840:400:::443
10-31 09:00:37.201  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:46696->2001:4860:…:443
10-31 09:00:37.201  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:46696->2001:4860:4844:400:::443
10-31 09:00:37.202  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41824->2001:4860:…:443
10-31 09:00:37.202  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:41824->2001:4860:4845:400:::443
10-31 09:00:37.204  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:54288->2001:4860:…:443
10-31 09:00:37.204  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:54288->2001:4860:4847:400:::443
10-31 09:00:37.221  3254  4485 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:53836->2001:4860:…:443
10-31 09:00:37.221  3254  4485 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:53836->2001:4860:4842:400:::443
10-31 09:00:37.231  3254  4485 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 09:00:37.282  3254  4860 D GhDiag  : flow_established 23ms
10-31 09:00:37.425  3254  4514 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=395
10-31 09:00:37.592  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 09:00:37.694  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55366->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6371 probe=false
10-31 09:00:37.723  3254  4863 D GhDiag  : flow_established 108ms
10-31 09:00:37.753  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 49228(3586KB) AllocSpace objects, 0(0B) LOS objects, 24% free, 9893KB/12MB, paused 7.231ms,24us total 396.807ms
10-31 09:00:37.864  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55386->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6154 probe=false
10-31 09:00:37.864  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55380->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6382 probe=false
10-31 09:00:37.920  3254  4485 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 09:00:38.087  3254  4874 D GhDiag  : flow_established 161ms
10-31 09:00:38.975  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55392->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6213 probe=false
10-31 09:00:39.335  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55394->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6500 probe=false
10-31 09:00:39.669   519   536 V WindowManager:     info={id=10 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{17da0a5 Task{d41f0ec #9 type=standard A=10150:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0xaa20b22 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{dbc16e2 Task{8a32eac #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0x94a88c4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 09:00:39.737  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:44304->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=7328 probe=false
10-31 09:00:39.940  3254  4488 D GhDiag  : flow_closed dst=fd00:1:…:55390->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7245 probe=false
10-31 09:00:39.948  3254  3322 I .ghprotocol.app: Background young concurrent copying GC freed 42199(3285KB) AllocSpace objects, 0(0B) LOS objects, 23% free, 10036KB/12MB, paused 69.001ms,36us total 509.943ms
10-31 09:00:40.340  3254  4488 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-48822 (4744) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:481) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.tick() for 194ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
