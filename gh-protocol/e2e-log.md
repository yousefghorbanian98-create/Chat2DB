## gh-protocol E2E log — 2026-10-31T08:54:26Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-31T08:51:55Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 31 08:49 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 31 08:52 .
drwxr-xr-x 3 runner runner 4096 Oct 31 08:52 ..
drwxr-xr-x 3 runner runner 4096 Oct 31 08:52 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 31 08:52 gh_test.ini

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
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15982 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15982 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.13.db, detection is enabled for process: 2991
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
WARNING: cannnot unmap ptr 0x7f47ba401000 as it is in the protected range from 0x7f46ba400000 to 0x7f47ba600000
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
INFO         | Boot completed in 46984 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 41
ERROR        | Failed to bind to texture: invalid color buffer.
ERROR        | Failed to find ColorBuffer: 114
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 2991) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll

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
> Task :app:extractDeepLinksDebug FROM-CACHE
> Task :app:generateDebugResources FROM-CACHE
> Task :app:mapDebugSourceSetPaths
> Task :app:packageDebugResources FROM-CACHE
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug FROM-CACHE
> Task :app:mergeDebugResources FROM-CACHE
> Task :app:desugarDebugFileDependencies FROM-CACHE
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:parseDebugLocalResources FROM-CACHE
> Task :app:mergeDebugJniLibFolders
> Task :app:processDebugManifestForPackage
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:compressDebugAssets FROM-CACHE
> Task :app:mergeLibDexDebug FROM-CACHE
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug FROM-CACHE
> Task :app:writeDebugAppMetadata
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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1793436659592.json

BUILD SUCCESSFUL in 1m
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
app up (try 1, pid 2970)
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
    inet6 fe80::6904:b9b2:12f0:6781/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.112.4): 56(84) bytes.

--- 140.82.112.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== in-tunnel payload self-test (the only accepted proof, requirement 5) ==
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
Starting service: Intent { act=com.ghprotocol.app.action.SELF_TEST cmp=com.ghprotocol.app/.core.VpnTunnelService }
Error: Requires permission not exported from uid 10192
relay self-test PASS (real remote payload through the relay)
10-31 08:54:15.276  2970  4248 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 08:54:15.277  2970  4248 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=898 firstByteMs=1009 checksums=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-31 08:54:16.037  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55346->2001:4860:4844:400:::443
10-31 08:54:16.086  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48584->2001:4860:…:443
10-31 08:54:16.086  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48584->2001:4860:4842:400:::443
10-31 08:54:16.093  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45342->2001:4860:…:443
10-31 08:54:16.093  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45342->2001:4860:4841:400:::443
10-31 08:54:16.111  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50598->2001:4860:…:443
10-31 08:54:16.112  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50598->2001:4860:4845:400:::443
10-31 08:54:16.121  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58180->2001:4860:…:443
10-31 08:54:16.124  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58180->2001:4860:4840:400:::443
10-31 08:54:16.206  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.211  2970  4679 D GhDiag  : flow_established 2ms
10-31 08:54:16.304  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58272->2001:4860:…:443
10-31 08:54:16.304  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58272->2001:4860:4846:400:::443
10-31 08:54:16.312  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55348->2001:4860:…:443
10-31 08:54:16.312  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55348->2001:4860:4844:400:::443
10-31 08:54:16.338  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57896->2001:4860:…:443
10-31 08:54:16.338  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57896->2001:4860:4847:400:::443
10-31 08:54:16.348  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48600->2001:4860:…:443
10-31 08:54:16.348  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48600->2001:4860:4842:400:::443
10-31 08:54:16.356  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45350->2001:4860:…:443
10-31 08:54:16.357  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45350->2001:4860:4841:400:::443
10-31 08:54:16.362  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50610->2001:4860:…:443
10-31 08:54:16.362  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50610->2001:4860:4845:400:::443
10-31 08:54:16.363  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58196->2001:4860:…:443
10-31 08:54:16.364  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58196->2001:4860:4840:400:::443
10-31 08:54:16.442  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57906->2001:4860:…:443
10-31 08:54:16.448  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57906->2001:4860:4847:400:::443
10-31 08:54:16.455  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=375
10-31 08:54:16.510  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56910->2001:4860:…:443
10-31 08:54:16.512  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56910->2001:4860:4843:400:::443
10-31 08:54:16.513  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56914->2001:4860:…:443
10-31 08:54:16.515  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56914->2001:4860:4843:400:::443
10-31 08:54:16.516  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.573  2970  4688 D GhDiag  : flow_established 9ms
10-31 08:54:17.011  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=495
10-31 08:54:17.096  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:17.168  2970  4699 D GhDiag  : flow_established 55ms
10-31 08:54:17.220  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35206->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6477 probe=false
10-31 08:54:17.528  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=511
10-31 08:54:17.745  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35190->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=7275 probe=false
10-31 08:54:18.059  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=529
10-31 08:54:18.111  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:18.138  2970  4739 D GhDiag  : flow_established 9ms
10-31 08:54:18.251  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=153
10-31 08:54:18.750  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=439
10-31 08:54:18.928  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:19.094  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34672->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6538 probe=false
10-31 08:54:19.112  2970  4758 D GhDiag  : flow_established 40ms
10-31 08:54:19.414  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58220->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6536 probe=false
10-31 08:54:19.616  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58224->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6371 probe=false
== real app traffic through the tunnel (requirement 5) ==
app traffic: appUp=65601 bytes
10-31 08:54:20.094  2970  4246 D GhDiag  : stats t=15s packets=315 tcp=254 dns53=14 otherUdp=20 activeTcp=13 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=65601 appDown=95804 probeUp=182 probeDown=804 probeFlows=1 dnsOk=14 dnsFail=0 state=VERIFIED ipv6=route_only
tunnel-local destinations are reset locally (no wasted upstream dial)
IPv6: route_only (tunnelled, payload NOT proven — no protection claimed)
10-31 08:54:15.276  2970  4248 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-31 08:53:55.012  2970  2970 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-31 08:53:55.012  2970  2970 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-31 08:53:55.393  2970  2970 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-31 08:53:55.518  2970  2970 I GhDiag  : effective_dns active Serverless-v52-fragA :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 08:53:55.518  2970  2970 I GhDiag  : effective_dns alternate Serverless-v52-fragB :: servers=https://cloudflare-dns.com/dns-query hosts=geosite:category-ads-all->#3,cloudflare-dns.com->104.16.248.249 strategy=UseIPv4 doh=https://cloudflare-dns.com/dns-query dohIps=104.16.248.249 dohOutbound=tcp-fragment-tls defaultOutbound=block notes=doh_bootstrap_zone_ok:cloudflare-dns.com->104.16.248.249
10-31 08:53:55.518  2970  2970 D GhDiag  : connect: config written bytes=5087 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-31 08:53:55.921  2970  2970 D GhDiag  : connect: core.start=true 
10-31 08:54:05.029  2970  2970 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-31 08:54:05.250  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 08:54:05.278  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-31 08:54:05.320  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 08:54:05.332  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.348  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.352  2970  4248 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 08:54:05.759  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.760  2970  4247 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 08:54:05.760  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:46850->fd00:1:…:853
10-31 08:54:05.763  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:46850->fd00:1::1:853
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=115
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=1274
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=156
10-31 08:54:05.817  2970  4247 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-31 08:54:05.817  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:06.086  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 08:54:06.106  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 08:54:06.139  2970  4278 D GhDiag  : flow_established 669ms
10-31 08:54:06.139  2970  4299 D GhDiag  : flow_established 311ms
10-31 08:54:06.141  2970  4247 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-31 08:54:06.146  2970  4247 D GhDiag  : flow_closed dst=fd00:1:…:48878->2001:4860:…:443 reason=client_rst up=0 down=0 ms=329 probe=false
10-31 08:54:06.276  2970  4248 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-31 08:54:06.292  2970  4312 D GhDiag  : flow_established 9ms
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=112
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:06.342  2970  4247 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 08:54:06.342  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:46856->fd00:1:…:853
10-31 08:54:06.342  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:46856->fd00:1::1:853
10-31 08:54:06.361  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 08:54:06.420  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 08:54:06.491  2970  4247 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-31 08:54:06.495  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:40054->10.8.x.x:853
10-31 08:54:06.498  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:40054->10.8.0.1:853
10-31 08:54:06.498  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:06.801  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=668
10-31 08:54:06.804  2970  4307 D GhDiag  : dns_reply 715ms path=doh:cloudflare-dns.com bytes=178
10-31 08:54:07.303  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=393
10-31 08:54:07.310  2970  4307 D GhDiag  : dns_reply 1203ms path=doh:cloudflare-dns.com bytes=274
10-31 08:54:07.512  2970  4315 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-31 08:54:07.537  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:07.541  2970  4315 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1270 probe=false
10-31 08:54:07.564  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:08.276  2970  4247 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=216
10-31 08:54:08.279  2970  4247 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=893
10-31 08:54:08.490  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-31 08:54:08.505  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-31 08:54:08.539  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:08.966  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=60
10-31 08:54:09.176  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=568
10-31 08:54:09.177  2970  4307 D GhDiag  : dns_reply 687ms path=doh:cloudflare-dns.com bytes=164
10-31 08:54:09.288  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=89
10-31 08:54:09.289  2970  4307 D GhDiag  : dns_reply 784ms path=doh:cloudflare-dns.com bytes=260
10-31 08:54:09.444  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:09.454  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:09.480  2970  4499 D GhDiag  : flow_established 2ms
10-31 08:54:09.483  2970  4500 D GhDiag  : flow_established 4ms
10-31 08:54:09.693  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=403
10-31 08:54:09.919  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=206
10-31 08:54:09.979  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:10.065  2970  4521 D GhDiag  : flow_established 16ms
10-31 08:54:10.080  2970  4246 D GhDiag  : stats t=5s packets=49 tcp=15 dns53=6 otherUdp=13 activeTcp=3 flowsOpened=6 flowsEstablished=6 connectFailures=0 retransmits=0 appUp=1413 appDown=3162 probeUp=91 probeDown=402 probeFlows=1 dnsOk=6 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 08:54:10.468  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:10.523  2970  4533 D GhDiag  : flow_established 17ms
10-31 08:54:10.742  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:10.976  2970  4545 D GhDiag  : flow_established 109ms
10-31 08:54:11.372  2970  4267 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=6028 probe=true
10-31 08:54:11.969  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=86
10-31 08:54:12.265  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=288
10-31 08:54:12.548  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:12.679  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:12.693  2970  4576 D GhDiag  : flow_established 67ms
10-31 08:54:12.877  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.051  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:13.076  2970  4581 D GhDiag  : flow_established 181ms
10-31 08:54:13.080  2970  4586 D GhDiag  : flow_established 39ms
10-31 08:54:13.245  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.397  2970  4598 D GhDiag  : flow_established 28ms
10-31 08:54:13.405  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.429  2970  4588 D GhDiag  : flow_established 164ms
10-31 08:54:13.458  2970  4247 D GhDiag  : flow_closed dst=10.8.x.x:44384->142.251.x.x:443 reason=client_rst up=0 down=0 ms=406 probe=false
10-31 08:54:13.510  2970  4604 D GhDiag  : flow_established 60ms
10-31 08:54:14.013  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:14.321  2970  4613 D GhDiag  : flow_established 200ms
10-31 08:54:14.329  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:14.460  2970  4620 D GhDiag  : flow_established 115ms
10-31 08:54:14.523  2970  4247 D GhDiag  : flow_closed dst=10.8.x.x:44388->142.251.x.x:443 reason=client_rst up=0 down=0 ms=193 probe=false
10-31 08:54:14.633  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:14.718  2970  4625 D GhDiag  : flow_established 71ms
10-31 08:54:15.061  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:15.089  2970  4246 D GhDiag  : stats t=10s packets=151 tcp=103 dns53=8 otherUdp=20 activeTcp=13 flowsOpened=18 flowsEstablished=17 connectFailures=0 retransmits=0 appUp=39601 appDown=8015 probeUp=91 probeDown=402 probeFlows=0 dnsOk=8 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 08:54:15.119  2970  4630 D GhDiag  : flow_established 47ms
10-31 08:54:15.255  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:15.275  2970  4248 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-31 08:54:15.276  2970  4248 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 08:54:15.277  2970  4248 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=898 firstByteMs=1009 checksums=0
10-31 08:54:15.293  2970  4638 D GhDiag  : flow_established 5ms
10-31 08:54:15.301  2970  4322 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 08:54:15.329  2970  4642 D GhDiag  : flow_established 14ms
10-31 08:54:15.412  2970  4322 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-31 08:54:15.414  2970  4322 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-31 08:54:15.684  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35184->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6240 probe=false
10-31 08:54:15.887  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58260->2001:4860:…:443
10-31 08:54:15.919  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58260->2001:4860:4846:400:::443
10-31 08:54:16.036  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55346->2001:4860:…:443
10-31 08:54:16.037  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55346->2001:4860:4844:400:::443
10-31 08:54:16.086  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48584->2001:4860:…:443
10-31 08:54:16.086  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48584->2001:4860:4842:400:::443
10-31 08:54:16.093  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45342->2001:4860:…:443
10-31 08:54:16.093  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45342->2001:4860:4841:400:::443
10-31 08:54:16.111  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50598->2001:4860:…:443
10-31 08:54:16.112  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50598->2001:4860:4845:400:::443
10-31 08:54:16.121  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58180->2001:4860:…:443
10-31 08:54:16.124  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58180->2001:4860:4840:400:::443
10-31 08:54:16.206  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.211  2970  4679 D GhDiag  : flow_established 2ms
10-31 08:54:16.304  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58272->2001:4860:…:443
10-31 08:54:16.304  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58272->2001:4860:4846:400:::443
10-31 08:54:16.312  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55348->2001:4860:…:443
10-31 08:54:16.312  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55348->2001:4860:4844:400:::443
10-31 08:54:16.338  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57896->2001:4860:…:443
10-31 08:54:16.338  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57896->2001:4860:4847:400:::443
10-31 08:54:16.348  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48600->2001:4860:…:443
10-31 08:54:16.348  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48600->2001:4860:4842:400:::443
10-31 08:54:16.356  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45350->2001:4860:…:443
10-31 08:54:16.357  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45350->2001:4860:4841:400:::443
10-31 08:54:16.362  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50610->2001:4860:…:443
10-31 08:54:16.362  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50610->2001:4860:4845:400:::443
10-31 08:54:16.363  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58196->2001:4860:…:443
10-31 08:54:16.364  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58196->2001:4860:4840:400:::443
10-31 08:54:16.442  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57906->2001:4860:…:443
10-31 08:54:16.448  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57906->2001:4860:4847:400:::443
10-31 08:54:16.455  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=375
10-31 08:54:16.510  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56910->2001:4860:…:443
10-31 08:54:16.512  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56910->2001:4860:4843:400:::443
10-31 08:54:16.513  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56914->2001:4860:…:443
10-31 08:54:16.515  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56914->2001:4860:4843:400:::443
10-31 08:54:16.516  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.573  2970  4688 D GhDiag  : flow_established 9ms
10-31 08:54:17.011  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=495
10-31 08:54:17.096  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:17.168  2970  4699 D GhDiag  : flow_established 55ms
10-31 08:54:17.220  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35206->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6477 probe=false
10-31 08:54:17.528  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=511
10-31 08:54:17.745  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35190->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=7275 probe=false
10-31 08:54:18.059  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=529
10-31 08:54:18.111  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:18.138  2970  4739 D GhDiag  : flow_established 9ms
10-31 08:54:18.251  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=153
10-31 08:54:18.750  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=439
10-31 08:54:18.928  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:19.094  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34672->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6538 probe=false
10-31 08:54:19.112  2970  4758 D GhDiag  : flow_established 40ms
10-31 08:54:19.414  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58220->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6536 probe=false
10-31 08:54:19.616  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58224->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6371 probe=false
10-31 08:54:20.094  2970  4246 D GhDiag  : stats t=15s packets=315 tcp=254 dns53=14 otherUdp=20 activeTcp=13 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=65601 appDown=95804 probeUp=182 probeDown=804 probeFlows=1 dnsOk=14 dnsFail=0 state=VERIFIED ipv6=route_only
10-31 08:54:20.317  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34682->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=7638 probe=false
10-31 08:54:20.424  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34686->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6410 probe=false
10-31 08:54:20.424  2970  4267 D GhDiag  : flow_closed dst=10.8.x.x:41002->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5132 probe=true
10-31 08:54:20.965  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58228->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7565 probe=false
10-31 08:54:21.156  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58238->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6523 probe=false
10-31 08:54:21.369  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58250->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6307 probe=false
10-31 08:54:21.374  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34692->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6118 probe=false
10-31 08:54:23.002  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=611
10-31 08:54:23.798  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=793
10-31 08:54:23.880  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:23.934  2970  4833 D GhDiag  : flow_established 7ms
10-31 08:54:24.414  2970  4322 D GhDiag  : relay_selftest_v6 ok=false stage=syn_ack detail=no_syn_ack
10-31 08:54:24.416  2970  4322 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=608 down=402 response=402 synAckMs=42 firstByteMs=118 checksums=0
10-31 08:54:24.534  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=156
10-31 08:54:24.638  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=74
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - in-tunnel payload self-test: PASS (real remote bytes through the relay)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
xf460c5 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{b56ecd4 u0 com.ghprotocol.app/.MainActivity)/@0x613ab3c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 08:53:58.609   839   872 V WindowManagerShell: Transition requested: android.os.BinderProxy@6b57ca7 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=67292 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@76b2554} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{f6acfd com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-31 08:53:59.144   523  2432 I ImeTracker: com.ghprotocol.app:ad00a45: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-31 08:53:59.144   523  2432 I ImeTracker: com.ghprotocol.app:ad00a45: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-31 08:53:59.149  1547  1547 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-31 08:53:59.557   523  1660 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-31 08:53:59.558   523  1660 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-31 08:53:59.558   523  1660 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-31 08:54:00.443   523   542 V WindowManager: Sent Transition #8 createdAt=10-31 08:53:58.493 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=67292 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{5e3c165 Task{239e7d #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{794ef2a com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-31 08:54:01.702  3990  3990 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-31 08:54:01.719  3990  3990 I AndroidRuntime: Using default boot image
10-31 08:54:01.723  3990  3990 I AndroidRuntime: Leaving lock profiling enabled
10-31 08:54:01.890   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{d831b77 com.google.android.googlequicksearchbox/10132} BLOCKED
10-31 08:54:01.890   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{83b23e4 com.android.camera2/10144} BLOCKED
10-31 08:54:01.891   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{c75f04d com.google.android.devicelockcontroller/10175} BLOCKED
10-31 08:54:01.891   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{5fcf702 com.google.android.contacts/10155} BLOCKED
10-31 08:54:01.891   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{1763204 com.google.android.projection.gearhead/10123} BLOCKED
10-31 08:54:01.972  3990  3990 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-31 08:54:03.086   523   538 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{5067a23 com.google.android.settings.intelligence/10118} BLOCKED
10-31 08:54:03.088   523  2557 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{70adb20 com.google.android.settings.intelligence/10118} BLOCKED
10-31 08:54:03.338  3990  3990 D AndroidRuntime: Shutting down VM
10-31 08:54:04.604   523  1660 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-31 08:54:04.846   523  1890 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-31 08:54:05.017   523  1890 I Vpn     : Established by com.ghprotocol.app on tun0
10-31 08:54:05.029  2970  2970 D GhDiag  : tun0 established ipv4=10.8.0.2/24 ipv6=fd00:1::2/64 route=::/0 state=route_only dns=10.8.0.1 mtu=1500
10-31 08:54:05.088   523  2862 I ImeTracker: com.ghprotocol.app:948c85de: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-31 08:54:05.088   523  2862 I ImeTracker: com.ghprotocol.app:948c85de: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-31 08:54:05.091  1547  1547 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-31 08:54:05.237  2970  4248 W .ghprotocol.app: Verification of void com.ghprotocol.app.core.net.TunnelSelfTest.<init>(com.ghprotocol.app.core.net.TcpRelay, java.lang.String, java.lang.String, kotlin.jvm.functions.Function0, int, kotlin.jvm.internal.DefaultConstructorMarker) took 100.687ms (248.29 bytecodes/s) (2000B approximate peak alloc)
10-31 08:54:05.250  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 08:54:05.278  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:2:…:0 len=48
10-31 08:54:05.320  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=76
10-31 08:54:05.332  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.348  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.352  2970  4248 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 08:54:05.759  2970  4247 D GhDiag  : tun v6 proto=58 dst=ff02:16:…:0 len=96
10-31 08:54:05.760  2970  4247 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 08:54:05.760  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:46850->fd00:1:…:853
10-31 08:54:05.763  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:46850->fd00:1::1:853
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=115
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=1274
10-31 08:54:05.763  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=156
10-31 08:54:05.817  2970  4247 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=80
10-31 08:54:05.817  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:06.086  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 08:54:06.106  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=78
10-31 08:54:06.129  2970  3003 I .ghprotocol.app: Background young concurrent copying GC freed 79447(4777KB) AllocSpace objects, 2(40KB) LOS objects, 41% free, 7295KB/12MB, paused 20us,96us total 174.989ms
10-31 08:54:06.139  2970  4278 D GhDiag  : flow_established 669ms
10-31 08:54:06.139  2970  4299 D GhDiag  : flow_established 311ms
10-31 08:54:06.141  2970  4247 D GhDiag  : tun v6 proto=6 dst=2001:4860:…:443 len=60
10-31 08:54:06.146  2970  4247 D GhDiag  : flow_closed dst=fd00:1:…:48878->2001:4860:…:443 reason=client_rst up=0 down=0 ms=329 probe=false
10-31 08:54:06.276  2970  4248 D GhDiag  : flow_open v6 dst=2606:4700:…:80 probe=false
10-31 08:54:06.292  2970  4312 D GhDiag  : flow_established 9ms
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=112
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:06.341  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:06.342  2970  4247 D GhDiag  : tun v6 proto=6 dst=fd00:1:…:853 len=84
10-31 08:54:06.342  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=fd00:1:…:46856->fd00:1:…:853
10-31 08:54:06.342  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination fd00:1::2:46856->fd00:1::1:853
10-31 08:54:06.361  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 08:54:06.420  2970  4247 D GhDiag  : tun v4 proto=17 dst=142.251.x.x:443 len=78
10-31 08:54:06.491  2970  4247 D GhDiag  : tun v4 proto=6 dst=10.8.x.x:853 len=60
10-31 08:54:06.495  2970  4247 D GhDiag  : flow_rejected reason=tunnel_local_destination dst=10.0.x.x:40054->10.8.x.x:853
10-31 08:54:06.498  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=local_destination 10.0.2.16:40054->10.8.0.1:853
10-31 08:54:06.498  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:06.801  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=668
10-31 08:54:06.804  2970  4307 D GhDiag  : dns_reply 715ms path=doh:cloudflare-dns.com bytes=178
10-31 08:54:07.303  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=393
10-31 08:54:07.310  2970  4307 D GhDiag  : dns_reply 1203ms path=doh:cloudflare-dns.com bytes=274
10-31 08:54:07.512  2970  4315 W GhDiag  : relay_warning stage=relay_reset detail=upstream_read_error:SocketException fd00:1::99:41001->2606:4700:4700::1111:80
10-31 08:54:07.537  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:07.541  2970  4315 D GhDiag  : flow_closed dst=fd00:1:…:41001->2606:4700:…:80 reason=upstream_read_error:SocketException up=91 down=0 ms=1270 probe=false
10-31 08:54:07.564  2970  4247 D GhDiag  : tun v6 proto=58 dst=2606:4700:…:0 len=108
10-31 08:54:07.571  2970  3002 I .ghprotocol.app: Compiler allocated 4290KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-31 08:54:08.036  2970  3003 I .ghprotocol.app: Background young concurrent copying GC freed 66557(4928KB) AllocSpace objects, 0(0B) LOS objects, 37% free, 7738KB/12MB, paused 59us,42us total 122.174ms
10-31 08:54:08.276  2970  4247 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=216
10-31 08:54:08.279  2970  4247 D GhDiag  : tun v4 proto=17 dst=172.217.x.x:443 len=893
10-31 08:54:08.490  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-31 08:54:08.505  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=64
10-31 08:54:08.539  2970  4247 D GhDiag  : tun v4 proto=1 dst=172.217.x.x:0 len=28
10-31 08:54:08.966  2970  4247 D GhDiag  : tun v4 proto=17 dst=10.8.x.x:53 len=60
10-31 08:54:09.164   523  1857 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4479, uid=2000 that is not exported from uid 10192
10-31 08:54:09.176  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=568
10-31 08:54:09.177  2970  4307 D GhDiag  : dns_reply 687ms path=doh:cloudflare-dns.com bytes=164
10-31 08:54:09.288  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=89
10-31 08:54:09.289  2970  4307 D GhDiag  : dns_reply 784ms path=doh:cloudflare-dns.com bytes=260
10-31 08:54:09.444  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:09.454  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:09.480  2970  4499 D GhDiag  : flow_established 2ms
10-31 08:54:09.483  2970  4500 D GhDiag  : flow_established 4ms
10-31 08:54:09.693  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=403
10-31 08:54:09.919  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=206
10-31 08:54:09.979  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:10.065  2970  4521 D GhDiag  : flow_established 16ms
10-31 08:54:10.080  2970  4246 D GhDiag  : stats t=5s packets=49 tcp=15 dns53=6 otherUdp=13 activeTcp=3 flowsOpened=6 flowsEstablished=6 connectFailures=0 retransmits=0 appUp=1413 appDown=3162 probeUp=91 probeDown=402 probeFlows=1 dnsOk=6 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 08:54:10.308  1472  2817 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-31 08:54:10.468  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:10.474  1429  3546 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-31 08:54:10.523  2970  4533 D GhDiag  : flow_established 17ms
10-31 08:54:10.742  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:10.976  2970  4545 D GhDiag  : flow_established 109ms
10-31 08:54:11.372  2970  4267 D GhDiag  : flow_closed dst=10.8.x.x:41000->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=6028 probe=true
10-31 08:54:11.413  2970  3003 I .ghprotocol.app: Background young concurrent copying GC freed 60713(4136KB) AllocSpace objects, 0(0B) LOS objects, 31% free, 8426KB/12MB, paused 737us,13us total 352.068ms
10-31 08:54:11.925   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{c31efc7 com.google.android.apps.messaging/10129} BLOCKED
10-31 08:54:11.925   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{33be9f4 com.google.android.gm/10140} BLOCKED
10-31 08:54:11.926   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{883251d com.google.android.rkpdapp/10187} BLOCKED
10-31 08:54:11.926   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{693d392 com.google.android.settings.intelligence/10118} BLOCKED
10-31 08:54:11.969  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=86
10-31 08:54:12.265  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=288
10-31 08:54:12.548  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:12.679  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:12.693  2970  4576 D GhDiag  : flow_established 67ms
10-31 08:54:12.877  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.051  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:13.076  2970  4581 D GhDiag  : flow_established 181ms
10-31 08:54:13.080  2970  4586 D GhDiag  : flow_established 39ms
10-31 08:54:13.245  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.397  2970  4598 D GhDiag  : flow_established 28ms
10-31 08:54:13.405  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:13.429  2970  4588 D GhDiag  : flow_established 164ms
10-31 08:54:13.458  2970  4247 D GhDiag  : flow_closed dst=10.8.x.x:44384->142.251.x.x:443 reason=client_rst up=0 down=0 ms=406 probe=false
10-31 08:54:13.471  2970  3003 I .ghprotocol.app: Background concurrent copying GC freed 58408(4618KB) AllocSpace objects, 34(680KB) LOS objects, 49% free, 8280KB/16MB, paused 166us,205us total 1.264s
10-31 08:54:13.510  2970  4604 D GhDiag  : flow_established 60ms
10-31 08:54:14.013  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:14.275   523   905 W ActivityManager: Permission Denial: Accessing service com.ghprotocol.app/.core.VpnTunnelService from pid=4614, uid=2000 that is not exported from uid 10192
10-31 08:54:14.321  2970  4613 D GhDiag  : flow_established 200ms
10-31 08:54:14.329  2970  4247 D GhDiag  : flow_open v4 dst=142.251.x.x:443 probe=false
10-31 08:54:14.460  2970  4620 D GhDiag  : flow_established 115ms
10-31 08:54:14.468  1630  1630 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-31 08:54:14.523  2970  4247 D GhDiag  : flow_closed dst=10.8.x.x:44388->142.251.x.x:443 reason=client_rst up=0 down=0 ms=193 probe=false
10-31 08:54:14.633  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:14.718  2970  4625 D GhDiag  : flow_established 71ms
10-31 08:54:15.061  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:15.089  2970  4246 D GhDiag  : stats t=10s packets=151 tcp=103 dns53=8 otherUdp=20 activeTcp=13 flowsOpened=18 flowsEstablished=17 connectFailures=0 retransmits=0 appUp=39601 appDown=8015 probeUp=91 probeDown=402 probeFlows=0 dnsOk=8 dnsFail=0 state=CORE_READY ipv6=route_only
10-31 08:54:15.109  1630  1630 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-31 08:54:15.119  2970  4630 D GhDiag  : flow_established 47ms
10-31 08:54:15.121  1630  2391 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-31 08:54:15.121  1630  2391 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-31 08:54:15.255  2970  4247 D GhDiag  : flow_open v6 dst=2001:4860:…:443 probe=false
10-31 08:54:15.275  2970  4248 D GhDiag  : ipv6_egress_unproven reason=no_payload_via_socks note=xray_dials_outside_the_tunnel_so_v6_needs_device_v6_egress action=reject_v6_flows_fast
10-31 08:54:15.276  2970  4248 D GhDiag  : relay_selftest_v6 ok=false stage=payload detail=no_response_bytes
10-31 08:54:15.277  2970  4248 D GhDiag  : relay_selftest ok=true stage=ok target=1.1.1.1:80 up=91 down=402 response=402 synAckMs=898 firstByteMs=1009 checksums=0
10-31 08:54:15.291  2970  4322 W .ghprotocol.app: Long monitor contention with owner gh-selftest (4248) at com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int)(TunnelSelfTest.kt:84) waiters=0 in com.ghprotocol.app.core.net.TunnelSelfTestResult com.ghprotocol.app.core.net.TunnelSelfTest.run(java.lang.String, int, byte[], kotlin.jvm.functions.Function1, int) for 8.695s
10-31 08:54:15.293  2970  4638 D GhDiag  : flow_established 5ms
10-31 08:54:15.301  2970  4322 D GhDiag  : flow_open v4 dst=1.1.x.x:80 probe=false
10-31 08:54:15.329  2970  4642 D GhDiag  : flow_established 14ms
10-31 08:54:15.412  2970  4322 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:41003->2606:4700:…:80
10-31 08:54:15.414  2970  4322 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::99:41003->2606:4700:4700::1111:80
10-31 08:54:15.684  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35184->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=6240 probe=false
10-31 08:54:15.887  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58260->2001:4860:…:443
10-31 08:54:15.919  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58260->2001:4860:4846:400:::443
10-31 08:54:16.036  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55346->2001:4860:…:443
10-31 08:54:16.037  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55346->2001:4860:4844:400:::443
10-31 08:54:16.086  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48584->2001:4860:…:443
10-31 08:54:16.086  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48584->2001:4860:4842:400:::443
10-31 08:54:16.093  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45342->2001:4860:…:443
10-31 08:54:16.093  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45342->2001:4860:4841:400:::443
10-31 08:54:16.111  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50598->2001:4860:…:443
10-31 08:54:16.112  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50598->2001:4860:4845:400:::443
10-31 08:54:16.121  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58180->2001:4860:…:443
10-31 08:54:16.124  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58180->2001:4860:4840:400:::443
10-31 08:54:16.206  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.211  2970  4679 D GhDiag  : flow_established 2ms
10-31 08:54:16.304  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58272->2001:4860:…:443
10-31 08:54:16.304  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58272->2001:4860:4846:400:::443
10-31 08:54:16.312  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:55348->2001:4860:…:443
10-31 08:54:16.312  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:55348->2001:4860:4844:400:::443
10-31 08:54:16.338  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57896->2001:4860:…:443
10-31 08:54:16.338  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57896->2001:4860:4847:400:::443
10-31 08:54:16.348  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:48600->2001:4860:…:443
10-31 08:54:16.348  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:48600->2001:4860:4842:400:::443
10-31 08:54:16.356  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:45350->2001:4860:…:443
10-31 08:54:16.357  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:45350->2001:4860:4841:400:::443
10-31 08:54:16.362  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:50610->2001:4860:…:443
10-31 08:54:16.362  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:50610->2001:4860:4845:400:::443
10-31 08:54:16.363  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:58196->2001:4860:…:443
10-31 08:54:16.364  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:58196->2001:4860:4840:400:::443
10-31 08:54:16.442  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:57906->2001:4860:…:443
10-31 08:54:16.448  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:57906->2001:4860:4847:400:::443
10-31 08:54:16.455  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=375
10-31 08:54:16.510  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56910->2001:4860:…:443
10-31 08:54:16.512  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56910->2001:4860:4843:400:::443
10-31 08:54:16.513  2970  4247 D GhDiag  : flow_rejected reason=ipv6_no_egress dst=fd00:1:…:56914->2001:4860:…:443
10-31 08:54:16.515  2970  4247 W GhDiag  : relay_warning stage=relay_reset detail=ipv6_no_egress fd00:1::2:56914->2001:4860:4843:400:::443
10-31 08:54:16.516  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:16.573  2970  4688 D GhDiag  : flow_established 9ms
10-31 08:54:17.011  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=495
10-31 08:54:17.096  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:17.168  2970  4699 D GhDiag  : flow_established 55ms
10-31 08:54:17.220  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35206->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6477 probe=false
10-31 08:54:17.528  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=511
10-31 08:54:17.745  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:35190->2001:4860:…:443 reason=half_close_complete up=805 down=0 ms=7275 probe=false
10-31 08:54:17.998  2970  3003 I .ghprotocol.app: Background young concurrent copying GC freed 102360(8386KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 8366KB/16MB, paused 415us,32us total 252.697ms
10-31 08:54:18.059  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=529
10-31 08:54:18.111  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:18.138  2970  4739 D GhDiag  : flow_established 9ms
10-31 08:54:18.251  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=153
10-31 08:54:18.750  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=439
10-31 08:54:18.928  2970  4247 D GhDiag  : flow_open v4 dst=172.217.x.x:443 probe=false
10-31 08:54:19.094  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34672->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=6538 probe=false
10-31 08:54:19.112  2970  4758 D GhDiag  : flow_established 40ms
10-31 08:54:19.414  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58220->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6536 probe=false
10-31 08:54:19.616  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58224->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6371 probe=false
10-31 08:54:20.094  2970  4246 D GhDiag  : stats t=15s packets=315 tcp=254 dns53=14 otherUdp=20 activeTcp=13 flowsOpened=25 flowsEstablished=25 connectFailures=0 retransmits=0 appUp=65601 appDown=95804 probeUp=182 probeDown=804 probeFlows=1 dnsOk=14 dnsFail=0 state=VERIFIED ipv6=route_only
10-31 08:54:20.317  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34682->2001:4860:…:443 reason=half_close_complete up=767 down=0 ms=7638 probe=false
10-31 08:54:20.424  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34686->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6410 probe=false
10-31 08:54:20.424  2970  4267 D GhDiag  : flow_closed dst=10.8.x.x:41002->1.1.x.x:80 reason=half_close_complete up=91 down=402 ms=5132 probe=true
10-31 08:54:20.965  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58228->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=7565 probe=false
10-31 08:54:21.156  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58238->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6523 probe=false
10-31 08:54:21.244   523   542 V WindowManager:     info={id=10 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{eb7dff8 Task{f5113f4 #9 type=standard A=10150:com.android.chrome}}} m=OPEN f=NONE leash=Surface(name=Task=9)/@0x9e78c86 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{5e3c165 Task{239e7d #8 type=standard A=10192:com.ghprotocol.app}}} m=TO_BACK f=NONE leash=Surface(name=Task=8)/@0x3b18d12 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-31 08:54:21.369  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:58250->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6307 probe=false
10-31 08:54:21.374  2970  4267 D GhDiag  : flow_closed dst=fd00:1:…:34692->2001:4860:…:443 reason=half_close_complete up=517 down=0 ms=6118 probe=false
10-31 08:54:22.097   523   578 I AppsFilter: interaction: PackageSetting{e774822 com.ghprotocol.app/10192} -> PackageSetting{66323ce com.google.android.contacts/10155} BLOCKED
10-31 08:54:22.115  2970  3003 W .ghprotocol.app: Suspending all threads took: 148.098ms
10-31 08:54:22.150  2970  3003 I .ghprotocol.app: Background young concurrent copying GC freed 107309(8408KB) AllocSpace objects, 0(0B) LOS objects, 46% free, 8818KB/16MB, paused 6.450ms,150.803ms total 353.502ms
10-31 08:54:23.002  2970  4307 D GhDiag  : dns_ok path=doh:cloudflare-dns.com ms=611

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
