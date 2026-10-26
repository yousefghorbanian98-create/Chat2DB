## gh-protocol E2E log — 2026-10-26T01:43:02Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-26T01:41:12Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 26 01:36 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 26 01:41 .
drwxr-xr-x 3 runner runner 4096 Oct 26 01:41 ..
drwxr-xr-x 3 runner runner 4096 Oct 26 01:41 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 26 01:41 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3104
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
WARNING: cannnot unmap ptr 0x7fdd0a801000 as it is in the protected range from 0x7fdc0a800000 to 0x7fdd0aa00000
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
INFO         | Boot completed in 39681 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 100
ERROR        | Failed to bind to texture: invalid color buffer.
ERROR        | Failed to find ColorBuffer: 109
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3104) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:44307 is gone due to Stream removed (CANCELLED)

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
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:packageDebugResources
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:parseDebugLocalResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeLibDexDebug
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug
> Task :app:processDebugResources
> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792978698740.json

BUILD SUCCESSFUL in 2m 47s
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
app up (try 1, pid 2705)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 2)
tunnel up after ~8s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
vpn established after ~3s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::2/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::2b38:f292:ee2:e1d9/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.3): 56(84) bytes.

--- 140.82.113.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
relay self-test PASS (real remote payload through the relay)
10-26 01:42:53.839  2705  4206 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:42:53.844  2705  4206 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=226 firstByteMs=295 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-26 01:42:51.754  2705  4570 D GhDiag  : flow_established 8ms
10-26 01:42:51.775  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.828  2705  4567 D GhDiag  : flow_closed dst=10.8.x.x:58356->172.217.x.x:443 reason=upstream_eof up=0 down=0 ms=223 probe=false
10-26 01:42:51.831  2705  4579 D GhDiag  : flow_established 2ms
10-26 01:42:52.881  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:52.903  2705  4619 D GhDiag  : flow_established 8ms
10-26 01:42:52.978  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.100  2705  4623 D GhDiag  : flow_established 19ms
10-26 01:42:53.803  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.829  2705  4645 D GhDiag  : flow_established 6ms
10-26 01:42:53.835  2705  4255 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:42:53.839  2705  4206 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:42:53.839  2705  4206 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:42:53.843  2705  4652 D GhDiag  : flow_established 2ms
10-26 01:42:53.844  2705  4206 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=226 firstByteMs=295 checksums=0
10-26 01:42:54.152  2705  4255 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:42:54.155  2705  4255 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:42:54.810  2705  4204 D GhDiag  : stats t=10s packets=188 tcp=165 dns53=4 otherUdp=5 activeTcp=14 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=56718 appDown=15360 probeUp=182 probeDown=804 probeFlows=1 dnsOk=4 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:42:55.154  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58236->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6224 probe=false
10-26 01:42:55.185  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58250->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6251 probe=false
10-26 01:42:55.186  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58256->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6253 probe=false
10-26 01:42:55.273  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=411
10-26 01:42:55.926  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=638
10-26 01:42:56.017  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.059  2705  4703 D GhDiag  : flow_established 5ms
10-26 01:42:56.284  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:42:56.422  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58260->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6346 probe=false
10-26 01:42:56.423  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58276->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6314 probe=false
10-26 01:42:56.434  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=149
10-26 01:42:56.436  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:47380->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:47380->2001:4860:482a:400:::443
10-26 01:42:56.437  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:59132->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:59132->2001:4860:4827:400:::443
10-26 01:42:56.438  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36188->2001:4860:…:443
10-26 01:42:56.439  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36188->2001:4860:4828:400:::443
10-26 01:42:56.439  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:33368->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:33368->2001:4860:482c:400:::443
10-26 01:42:56.440  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:49948->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:49948->2001:4860:482d:400:::443
10-26 01:42:56.441  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:51456->2001:4860:…:443
10-26 01:42:56.443  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:51456->2001:4860:4826:400:::443
10-26 01:42:56.444  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36992->2001:4860:…:443
10-26 01:42:56.445  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36992->2001:4860:4829:400:::443
10-26 01:42:56.445  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37016->2001:4860:…:443
10-26 01:42:56.446  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37016->2001:4860:482b:400:::443
10-26 01:42:56.446  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:42:56.493  2705  4711 D GhDiag  : flow_established 13ms
10-26 01:42:56.526  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58278->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6399 probe=false
10-26 01:42:56.541  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.554  2705  4716 D GhDiag  : flow_established 2ms
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=56718 bytes
10-26 01:42:54.810  2705  4204 D GhDiag  : stats t=10s packets=188 tcp=165 dns53=4 otherUdp=5 activeTcp=14 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=56718 appDown=15360 probeUp=182 probeDown=804 probeFlows=1 dnsOk=4 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-26 01:42:53.839  2705  4206 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-26 01:42:34.557  2705  2705 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-26 01:42:34.557  2705  2705 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-26 01:42:34.873  2705  2705 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-26 01:42:35.038  2705  2705 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:42:35.038  2705  2705 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-26 01:42:35.038  2705  2705 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-26 01:42:35.697  2705  2705 D GhDiag  : connect: core.start=true 
10-26 01:42:44.503  2705  2705 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:44.717  2705  4206 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:42:44.746  2705  4210 D GhDiag  : flow_established 17ms
10-26 01:42:44.831  2705  4206 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:42:44.922  2705  4215 D GhDiag  : flow_established 27ms
10-26 01:42:45.289  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:45.304  2705  4205 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:42:45.304  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:44976->fd00:1:…:853
10-26 01:42:45.307  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:44976->fd00:1::1:853
10-26 01:42:45.400  2705  4205 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:42:45.430  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.438  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:42:45.442  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:42:45.500  2705  4257 D GhDiag  : flow_established 24ms
10-26 01:42:45.501  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.504  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=557
10-26 01:42:45.581  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.583  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.584  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.585  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=114
10-26 01:42:45.590  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=132
10-26 01:42:45.591  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=335
10-26 01:42:45.599  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=71
10-26 01:42:45.616  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.619  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.642  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=75
10-26 01:42:45.970  2705  4205 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:42:45.977  2705  4230 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:42:45.980  2705  4230 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1146 probe=false
10-26 01:42:45.981  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:47114->10.8.x.x:853
10-26 01:42:46.011  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:47114->10.8.0.1:853
10-26 01:42:46.018  2705  4205 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:42:46.155  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.180  2705  4261 D GhDiag  : flow_closed dst=10.8.x.x:49158->142.251.x.x:443 reason=upstream_eof up=1044 down=5908 ms=738 probe=false
10-26 01:42:46.181  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.181  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.362  2705  4205 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:42:46.624  2705  4205 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:42:46.625  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:44992->fd00:1:…:853
10-26 01:42:46.626  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:44992->fd00:1::1:853
10-26 01:42:46.633  2705  4205 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:42:46.633  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:40088->10.8.x.x:853
10-26 01:42:46.634  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:40088->10.8.0.1:853
10-26 01:42:46.893  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:48.173  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=667
10-26 01:42:48.173  2705  4411 D GhDiag  : dns_reply 721ms path=doh:cloudflare-dns.com bytes=260
10-26 01:42:48.800  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=618
10-26 01:42:48.928  2705  4411 D GhDiag  : dns_reply 1476ms path=doh:cloudflare-dns.com bytes=164
10-26 01:42:48.930  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:48.932  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:48.933  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:48.933  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:49.027  2705  4510 D GhDiag  : flow_established 17ms
10-26 01:42:49.034  2705  4511 D GhDiag  : flow_established 22ms
10-26 01:42:49.043  2705  4512 D GhDiag  : flow_established 14ms
10-26 01:42:49.054  2705  4513 D GhDiag  : flow_established 23ms
10-26 01:42:49.127  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=198
10-26 01:42:49.774  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=532
10-26 01:42:49.809  2705  4204 D GhDiag  : stats t=5s packets=79 tcp=64 dns53=4 otherUdp=3 activeTcp=4 flowsOpened=7 flowsEstablished=7 connectFailures=0 retransmits=0 appUp=34918 appDown=9073 probeUp=91 probeDown=402 probeFlows=1 dnsOk=4 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:42:50.040  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:50.075  2705  4535 D GhDiag  : flow_established 25ms
10-26 01:42:50.076  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.101  2705  4539 D GhDiag  : flow_established 16ms
10-26 01:42:50.110  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.126  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.146  2705  4209 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5429 probe=true
10-26 01:42:50.241  2705  4543 D GhDiag  : flow_established 30ms
10-26 01:42:50.259  2705  4544 D GhDiag  : flow_established 30ms
10-26 01:42:51.228  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.524  2705  4556 D GhDiag  : flow_established 292ms
10-26 01:42:51.605  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:51.660  2705  4565 D GhDiag  : flow_established 3ms
10-26 01:42:51.718  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.754  2705  4570 D GhDiag  : flow_established 8ms
10-26 01:42:51.775  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.828  2705  4567 D GhDiag  : flow_closed dst=10.8.x.x:58356->172.217.x.x:443 reason=upstream_eof up=0 down=0 ms=223 probe=false
10-26 01:42:51.831  2705  4579 D GhDiag  : flow_established 2ms
10-26 01:42:52.881  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:52.903  2705  4619 D GhDiag  : flow_established 8ms
10-26 01:42:52.978  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.100  2705  4623 D GhDiag  : flow_established 19ms
10-26 01:42:53.803  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.829  2705  4645 D GhDiag  : flow_established 6ms
10-26 01:42:53.835  2705  4255 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:42:53.839  2705  4206 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:42:53.839  2705  4206 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:42:53.843  2705  4652 D GhDiag  : flow_established 2ms
10-26 01:42:53.844  2705  4206 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=226 firstByteMs=295 checksums=0
10-26 01:42:54.152  2705  4255 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:42:54.155  2705  4255 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:42:54.810  2705  4204 D GhDiag  : stats t=10s packets=188 tcp=165 dns53=4 otherUdp=5 activeTcp=14 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=56718 appDown=15360 probeUp=182 probeDown=804 probeFlows=1 dnsOk=4 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:42:55.154  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58236->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6224 probe=false
10-26 01:42:55.185  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58250->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6251 probe=false
10-26 01:42:55.186  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58256->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6253 probe=false
10-26 01:42:55.273  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=411
10-26 01:42:55.926  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=638
10-26 01:42:56.017  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.059  2705  4703 D GhDiag  : flow_established 5ms
10-26 01:42:56.284  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:42:56.422  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58260->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6346 probe=false
10-26 01:42:56.423  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58276->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6314 probe=false
10-26 01:42:56.434  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=149
10-26 01:42:56.436  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:47380->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:47380->2001:4860:482a:400:::443
10-26 01:42:56.437  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:59132->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:59132->2001:4860:4827:400:::443
10-26 01:42:56.438  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36188->2001:4860:…:443
10-26 01:42:56.439  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36188->2001:4860:4828:400:::443
10-26 01:42:56.439  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:33368->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:33368->2001:4860:482c:400:::443
10-26 01:42:56.440  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:49948->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:49948->2001:4860:482d:400:::443
10-26 01:42:56.441  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:51456->2001:4860:…:443
10-26 01:42:56.443  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:51456->2001:4860:4826:400:::443
10-26 01:42:56.444  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36992->2001:4860:…:443
10-26 01:42:56.445  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36992->2001:4860:4829:400:::443
10-26 01:42:56.445  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37016->2001:4860:…:443
10-26 01:42:56.446  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37016->2001:4860:482b:400:::443
10-26 01:42:56.446  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:42:56.493  2705  4711 D GhDiag  : flow_established 13ms
10-26 01:42:56.526  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58278->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6399 probe=false
10-26 01:42:56.541  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.554  2705  4716 D GhDiag  : flow_established 2ms
10-26 01:42:57.947  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50312->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6230 probe=false
10-26 01:42:57.948  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50324->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6173 probe=false
10-26 01:42:58.137  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=605
10-26 01:42:58.925  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58284->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=7697 probe=false
10-26 01:42:59.049  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50330->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6169 probe=false
10-26 01:42:59.129  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=928
10-26 01:42:59.152  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50346->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6174 probe=false
10-26 01:42:59.170  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:59.267  2705  4209 D GhDiag  : flow_closed dst=10.8.x.x:41002->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5432 probe=true
10-26 01:42:59.343  2705  4773 D GhDiag  : flow_established 19ms
10-26 01:42:59.767  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=244
10-26 01:42:59.815  2705  4204 D GhDiag  : stats t=15s packets=312 tcp=272 dns53=12 otherUdp=8 activeTcp=7 flowsOpened=23 flowsEstablished=23 connectFailures=0 retransmits=0 appUp=76709 appDown=73699 probeUp=182 probeDown=804 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:42:59.889  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50360->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6086 probe=false
10-26 01:43:00.001  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=230
10-26 01:43:00.101  2705  4205 D GhDiag  : flow_open v4 dst=172.253.x.x:443 probe=false
10-26 01:43:00.116  2705  4801 D GhDiag  : flow_established 2ms
10-26 01:43:00.146  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=144
10-26 01:43:00.240  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=87
10-26 01:43:00.249  2705  4205 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-26 01:43:00.376  2705  4808 D GhDiag  : flow_established 4ms
10-26 01:43:00.429  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=125
10-26 01:43:00.589  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=154
10-26 01:43:00.606  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:43:00.659  2705  4823 D GhDiag  : flow_established 15ms
10-26 01:43:01.011  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=175
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
 com.ghprotocol.app/.MainActivity)/@0xcc30ee4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:42:38.532   832   868 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{17a7fa2 u0 com.ghprotocol.app/.MainActivity)/@0xedbd277 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{31338d2 u0 com.ghprotocol.app/.MainActivity)/@0xcc30ee4 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:42:38.763   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +4s308ms
10-26 01:42:38.763   519   536 V WindowManager: Sent Transition #7 createdAt=10-26 01:42:34.283 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=53620 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6807d92 Task{7683030 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d7aecb3 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:42:38.764   519   536 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{17a7fa2 u0 com.ghprotocol.app/.MainActivity)/@0x6141b2 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{31338d2 u0 com.ghprotocol.app/.MainActivity)/@0xfc6f7bd sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:42:38.847   832   868 V WindowManagerShell: Transition requested: android.os.BinderProxy@a11281 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=57829 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@8fe5f26} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2b04767 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:42:39.082   519   539 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{17a7fa2 u0 com.ghprotocol.app/.MainActivity t8}
10-26 01:42:39.088   519   539 W ActivityTaskManager: Activity pause timeout for ActivityRecord{17a7fa2 u0 com.ghprotocol.app/.MainActivity t8}
10-26 01:42:39.363   519  2419 I ImeTracker: com.ghprotocol.app:8c979714: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-26 01:42:39.364   519  2419 I ImeTracker: com.ghprotocol.app:8c979714: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:42:39.396  1557  1557 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:42:39.575   519  1942 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-26 01:42:39.578   519  1942 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-26 01:42:39.578   519  1942 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-26 01:42:40.445   519   536 V WindowManager: Sent Transition #8 createdAt=10-26 01:42:38.557 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=57829 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6807d92 Task{7683030 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{cbb3d15 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-26 01:42:40.834  1420  3366 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-26 01:42:41.357  3869  3869 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-26 01:42:41.381  3869  3869 I AndroidRuntime: Using default boot image
10-26 01:42:41.381  3869  3869 I AndroidRuntime: Leaving lock profiling enabled
10-26 01:42:41.841  3869  3869 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-26 01:42:42.466   519  2004 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{dd7fef7 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:42:42.466   519  2418 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{eb10164 com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:42:42.610  1471  3549 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-26 01:42:43.069  3869  3869 D AndroidRuntime: Shutting down VM
10-26 01:42:44.282   519  2004 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-26 01:42:44.449   519  1380 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-26 01:42:44.498   519   533 I Vpn     : Established by com.ghprotocol.app on tun0
10-26 01:42:44.503  2705  2705 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-26 01:42:44.695  1686  1686 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-26 01:42:44.698  1686  3456 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-26 01:42:44.698  1686  3456 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-26 01:42:44.700  2705  4206 W .ghprotocol.app: Verification of boolean com.ghprotocol.app.core.net.PacketCodec.isIpLiteral(java.lang.String) took 174.385ms (1003.53 bytecodes/s) (6096B approximate peak alloc)
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:44.702  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:44.717  2705  4206 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:42:44.746  2705  4210 D GhDiag  : flow_established 17ms
10-26 01:42:44.831  2705  4206 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-26 01:42:44.922  2705  4215 D GhDiag  : flow_established 27ms
10-26 01:42:45.077   519   533 I ImeTracker: com.ghprotocol.app:a559b86: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-26 01:42:45.080   519   533 I ImeTracker: com.ghprotocol.app:a559b86: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-26 01:42:45.095  1557  1557 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-26 01:42:45.289  2705  4205 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-26 01:42:45.304  2705  4205 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:42:45.304  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:44976->fd00:1:…:853
10-26 01:42:45.307  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:44976->fd00:1::1:853
10-26 01:42:45.318   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{615169d com.google.android.googlequicksearchbox/10132} BLOCKED
10-26 01:42:45.318   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{e4ca712 com.android.camera2/10145} BLOCKED
10-26 01:42:45.319   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{b76cee3 com.google.android.gm/10140} BLOCKED
10-26 01:42:45.319   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{b3170e0 com.google.android.devicelockcontroller/10191} BLOCKED
10-26 01:42:45.319   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{1b17f99 com.google.android.rkpdapp/10185} BLOCKED
10-26 01:42:45.320   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{6ca225e com.google.android.settings.intelligence/10118} BLOCKED
10-26 01:42:45.320   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{78ff7b6 com.google.android.projection.gearhead/10123} BLOCKED
10-26 01:42:45.400  2705  4205 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=61
10-26 01:42:45.430  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.438  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=60
10-26 01:42:45.442  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:42:45.500  2705  4257 D GhDiag  : flow_established 24ms
10-26 01:42:45.501  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.504  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=557
10-26 01:42:45.581  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.583  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.584  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.585  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=114
10-26 01:42:45.590  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=132
10-26 01:42:45.591  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=335
10-26 01:42:45.599  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=71
10-26 01:42:45.616  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.619  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:45.642  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=75
10-26 01:42:45.970  2705  4205 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-26 01:42:45.977  2705  4230 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-26 01:42:45.980  2705  4230 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1146 probe=false
10-26 01:42:45.981  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:47114->10.8.x.x:853
10-26 01:42:46.011  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:47114->10.8.0.1:853
10-26 01:42:46.018  2705  4205 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-26 01:42:46.155  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.180  2705  4261 D GhDiag  : flow_closed dst=10.8.x.x:49158->142.251.x.x:443 reason=upstream_eof up=1044 down=5908 ms=738 probe=false
10-26 01:42:46.181  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.181  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:46.324  2705  2713 I .ghprotocol.app: Background young concurrent copying GC freed 85072(5430KB) AllocSpace objects, 2(40KB) LOS objects, 40% free, 7737KB/12MB, paused 33us,11us total 461.860ms
10-26 01:42:46.362  2705  4205 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-26 01:42:46.410  2705  2712 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-26 01:42:46.624  2705  4205 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-26 01:42:46.625  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:44992->fd00:1:…:853
10-26 01:42:46.626  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:44992->fd00:1::1:853
10-26 01:42:46.633  2705  4205 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=64
10-26 01:42:46.633  2705  4205 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.8.x.x:40088->10.8.x.x:853
10-26 01:42:46.634  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.8.0.2:40088->10.8.0.1:853
10-26 01:42:46.893  2705  4205 D GhDiag  : tun v4 proto=6 dst=142.251.x.x:443 len=40
10-26 01:42:48.173  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=667
10-26 01:42:48.173  2705  4411 D GhDiag  : dns_reply 721ms path=doh:cloudflare-dns.com bytes=260
10-26 01:42:48.295   519  2004 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4488, uid=2000 that is not exported from uid 10192
10-26 01:42:48.800  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=618
10-26 01:42:48.928  2705  4411 D GhDiag  : dns_reply 1476ms path=doh:cloudflare-dns.com bytes=164
10-26 01:42:48.930  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:48.932  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:48.933  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:48.933  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:49.027  2705  4510 D GhDiag  : flow_established 17ms
10-26 01:42:49.034  2705  4511 D GhDiag  : flow_established 22ms
10-26 01:42:49.043  2705  4512 D GhDiag  : flow_established 14ms
10-26 01:42:49.054  2705  4513 D GhDiag  : flow_established 23ms
10-26 01:42:49.127  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=198
10-26 01:42:49.774  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=532
10-26 01:42:49.809  2705  4204 D GhDiag  : stats t=5s packets=79 tcp=64 dns53=4 otherUdp=3 activeTcp=4 flowsOpened=7 flowsEstablished=7 connectFailures=0 retransmits=0 appUp=34918 appDown=9073 probeUp=91 probeDown=402 probeFlows=1 dnsOk=4 dnsFail=0 state=CORE_READY ipv6=route_only
10-26 01:42:50.040  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:50.045  2705  4209 W .ghprotocol.app: Long monitor contention with owner gh-relay-rx-34672 (4521) at void com.ghprotocol.app.core.net.TcpRelay.onUpstreamData(com.ghprotocol.app.core.net.TcpRelay$Flow, byte[], int)(TcpRelay.kt:481) waiters=0 in void com.ghprotocol.app.core.net.TcpRelay.tick() for 236ms
10-26 01:42:50.075  2705  4535 D GhDiag  : flow_established 25ms
10-26 01:42:50.076  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.101  2705  4539 D GhDiag  : flow_established 16ms
10-26 01:42:50.110  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.126  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:50.146  2705  4209 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5429 probe=true
10-26 01:42:50.241  2705  4543 D GhDiag  : flow_established 30ms
10-26 01:42:50.259  2705  4544 D GhDiag  : flow_established 30ms
10-26 01:42:51.228  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.524  2705  4556 D GhDiag  : flow_established 292ms
10-26 01:42:51.605  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:51.660  2705  4565 D GhDiag  : flow_established 3ms
10-26 01:42:51.718  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.754  2705  4570 D GhDiag  : flow_established 8ms
10-26 01:42:51.775  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:51.828  2705  4567 D GhDiag  : flow_closed dst=10.8.x.x:58356->172.217.x.x:443 reason=upstream_eof up=0 down=0 ms=223 probe=false
10-26 01:42:51.831  2705  4579 D GhDiag  : flow_established 2ms
10-26 01:42:52.573   519  1172 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4612, uid=2000 that is not exported from uid 10192
10-26 01:42:52.881  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:52.903  2705  4619 D GhDiag  : flow_established 8ms
10-26 01:42:52.978  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.100  2705  4623 D GhDiag  : flow_established 19ms
10-26 01:42:53.803  2705  4205 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-26 01:42:53.829  2705  4645 D GhDiag  : flow_established 6ms
10-26 01:42:53.835  2705  4255 W .ghprotocol.app: Long monitor contention with owner gh-selftest (4206) at com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int)(TunnelSelfTest.kt:84) waiters=0 in com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int) for 8.601s
10-26 01:42:53.835  2705  4255 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-26 01:42:53.839  2705  4206 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-26 01:42:53.839  2705  4206 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-26 01:42:53.843  2705  4652 D GhDiag  : flow_established 2ms
10-26 01:42:53.844  2705  4206 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=226 firstByteMs=295 checksums=0
10-26 01:42:54.152  2705  4255 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-26 01:42:54.155  2705  4255 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-26 01:42:54.471  2705  2713 I .ghprotocol.app: Background young concurrent copying GC freed 80116(6871KB) AllocSpace objects, 0(0B) LOS objects, 42% free, 8373KB/14MB, paused 43us,23us total 320.350ms
10-26 01:42:54.810  2705  4204 D GhDiag  : stats t=10s packets=188 tcp=165 dns53=4 otherUdp=5 activeTcp=14 flowsOpened=19 flowsEstablished=19 connectFailures=0 retransmits=0 appUp=56718 appDown=15360 probeUp=182 probeDown=804 probeFlows=1 dnsOk=4 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:42:55.154  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58236->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6224 probe=false
10-26 01:42:55.185  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58250->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6251 probe=false
10-26 01:42:55.186  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58256->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6253 probe=false
10-26 01:42:55.273  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=411
10-26 01:42:55.632   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{d93f65 com.google.android.apps.messaging/10130} BLOCKED
10-26 01:42:55.632   519   570 I AppsFilter: interaction: PackageSetting{36e88c4 com.ghprotocol.app/10192} -> PackageSetting{aeef43a com.google.android.gm/10140} BLOCKED
10-26 01:42:55.926  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=638
10-26 01:42:56.017  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.059  2705  4703 D GhDiag  : flow_established 5ms
10-26 01:42:56.082  2705  2713 I .ghprotocol.app: Background concurrent copying GC freed 99287(7560KB) AllocSpace objects, 12(240KB) LOS objects, 49% free, 7987KB/15MB, paused 61us,19us total 287.491ms
10-26 01:42:56.284  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=311
10-26 01:42:56.422  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58260->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6346 probe=false
10-26 01:42:56.423  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58276->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6314 probe=false
10-26 01:42:56.434  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=149
10-26 01:42:56.436  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:47380->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:47380->2001:4860:482a:400:::443
10-26 01:42:56.437  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:59132->2001:4860:…:443
10-26 01:42:56.437  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:59132->2001:4860:4827:400:::443
10-26 01:42:56.438  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36188->2001:4860:…:443
10-26 01:42:56.439  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36188->2001:4860:4828:400:::443
10-26 01:42:56.439  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:33368->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:33368->2001:4860:482c:400:::443
10-26 01:42:56.440  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:49948->2001:4860:…:443
10-26 01:42:56.440  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:49948->2001:4860:482d:400:::443
10-26 01:42:56.441  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:51456->2001:4860:…:443
10-26 01:42:56.443  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:51456->2001:4860:4826:400:::443
10-26 01:42:56.444  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:36992->2001:4860:…:443
10-26 01:42:56.445  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:36992->2001:4860:4829:400:::443
10-26 01:42:56.445  2705  4205 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:37016->2001:4860:…:443
10-26 01:42:56.446  2705  4205 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:37016->2001:4860:482b:400:::443
10-26 01:42:56.446  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:42:56.493  2705  4711 D GhDiag  : flow_established 13ms
10-26 01:42:56.526  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58278->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6399 probe=false
10-26 01:42:56.541  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:56.554  2705  4716 D GhDiag  : flow_established 2ms
10-26 01:42:57.947  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50312->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6230 probe=false
10-26 01:42:57.948  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50324->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6173 probe=false
10-26 01:42:58.137  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=605
10-26 01:42:58.925  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:58284->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=7697 probe=false
10-26 01:42:58.998   519   536 V WindowManager:     info={id=10 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{927b57 Task{ded31f1 #9 type=standard A=10150:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0x8bf8605 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{6807d92 Task{7683030 #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0xb896826 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-26 01:42:59.049  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50330->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6169 probe=false
10-26 01:42:59.129  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=928
10-26 01:42:59.152  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50346->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6174 probe=false
10-26 01:42:59.170  2705  4205 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-26 01:42:59.267  2705  4209 D GhDiag  : flow_closed dst=10.8.x.x:41002->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5432 probe=true
10-26 01:42:59.343  2705  4773 D GhDiag  : flow_established 19ms
10-26 01:42:59.767  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=244
10-26 01:42:59.815  2705  4204 D GhDiag  : stats t=15s packets=312 tcp=272 dns53=12 otherUdp=8 activeTcp=7 flowsOpened=23 flowsEstablished=23 connectFailures=0 retransmits=0 appUp=76709 appDown=73699 probeUp=182 probeDown=804 probeFlows=0 dnsOk=11 dnsFail=0 state=VERIFIED ipv6=route_only
10-26 01:42:59.889  2705  4209 D GhDiag  : flow_closed dst=fd00:1:…:50360->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6086 probe=false
10-26 01:43:00.001  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=230
10-26 01:43:00.101  2705  4205 D GhDiag  : flow_open v4 dst=172.253.x.x:443 probe=false
10-26 01:43:00.116  2705  4801 D GhDiag  : flow_established 2ms
10-26 01:43:00.146  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=144
10-26 01:43:00.240  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=87
10-26 01:43:00.249  2705  4205 D GhDiag  : flow_open v4 dst=192.178.x.x:443 probe=false
10-26 01:43:00.376  2705  4808 D GhDiag  : flow_established 4ms
10-26 01:43:00.429  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=125
10-26 01:43:00.589  2705  4411 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=154
10-26 01:43:00.606  2705  4205 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-26 01:43:00.659  2705  4823 D GhDiag  : flow_established 15ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
