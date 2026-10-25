## gh-protocol E2E log — 2026-10-25T18:10:49Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T18:09:07Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 18:04 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 18:09 .
drwxr-xr-x 3 runner runner 4096 Oct 25 18:09 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 18:09 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 18:09 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3161
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
WARNING: cannnot unmap ptr 0x7fc7b6e01000 as it is in the protected range from 0x7fc6b6e00000 to 0x7fc7b7000000
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
INFO         | Boot completed in 38132 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
INFO         | Wait for emulator (pid 3161) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:37461 is gone due to Stream removed (CANCELLED)

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
> Task :app:mergeDebugAssets
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:compressDebugAssets
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:539:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792951563473.json

BUILD SUCCESSFUL in 2m 53s
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
app up (try 1, pid 2962)
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
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::5e94:d63d:b390:3d19/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.3): 56(84) bytes.

--- 140.82.113.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 18:10:31.502  2962  2962 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:10:31.517  2962  2962 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:10:31.838  2962  2962 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:10:31.931  2962  2962 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:10:32.240  2962  2962 D GhDiag  : connect: core.start=true 
10-25 18:10:42.172  2962  2962 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:10:42.248  2962  2962 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@db09da2} — relay loop started
10-25 18:10:42.524  2962  3265 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (56ms)
10-25 18:10:43.494  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.532  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:43.628  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.652  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.705  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:10:44.051  2962  4412 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:10:44.135  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:44.554  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:44.999  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:45.262  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.266  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.352  2962  4445 D GhDiag  : relay dns -> 168B ok
10-25 18:10:45.361  2962  4444 D GhDiag  : relay dns -> 264B ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 18:10:31.502  2962  2962 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:10:31.517  2962  2962 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:10:31.838  2962  2962 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:10:31.931  2962  2962 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:10:32.240  2962  2962 D GhDiag  : connect: core.start=true 
10-25 18:10:42.172  2962  2962 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:10:42.248  2962  2962 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@db09da2} — relay loop started
10-25 18:10:42.524  2962  3265 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (56ms)
10-25 18:10:43.494  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.532  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:43.628  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.652  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.705  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:10:44.051  2962  4412 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:10:44.135  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:44.554  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:44.999  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:45.262  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.266  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.352  2962  4445 D GhDiag  : relay dns -> 168B ok
10-25 18:10:45.361  2962  4444 D GhDiag  : relay dns -> 264B ok
10-25 18:10:45.518  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 18:10:45.523  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 18:10:45.525  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 18:10:45.656  2962  4479 D GhDiag  : relay dns -> 177B ok
10-25 18:10:45.673  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:45.785  2962  4477 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:10:45.786  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.810  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 18:10:45.841  2962  4488 D GhDiag  : relay dns -> 273B ok
10-25 18:10:45.878  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.949  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 18:10:45.981  2962  4512 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:10:45.982  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.992  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 18:10:46.632  2962  4573 D GhDiag  : relay dns -> 85B ok
10-25 18:10:46.700  2962  4574 D GhDiag  : relay dns -> 61B ok
10-25 18:10:46.774  2962  4585 D GhDiag  : relay tcp 192.178.x.x:443 -> socks5 ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
omponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=44244 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@f11cdf1} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{ba4dd6 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:23.064   519  2332 D CoreBackPreview: Window{427f7d0 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@2b32385, mPriority=0, mIsAnimationCallback=false}
10-25 18:10:23.203   519   550 I ActivityManager: Start proc 2962:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 18:10:23.206  2962  2962 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 18:10:23.219  2962  2962 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 18:10:23.219  2962  2962 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 18:10:23.219  2962  2962 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 18:10:23.498   519   537 V WindowManager: Sent Transition #6 createdAt=10-25 18:10:22.994 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=44244 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{dc6c486 Task{f9507b3 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{326b147 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:23.499   519   537 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{dc6c486 Task{f9507b3 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xc7abbe5 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{24d829d Task{435a8e4 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xe478173 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:10:24.044  2962  2962 W ziparchive: Unable to open '/data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/base.dm': No such file or directory
10-25 18:10:24.045  2962  2962 W ziparchive: Unable to open '/data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/base.dm': No such file or directory
10-25 18:10:24.568  2962  2962 D nativeloader: Configuring clns-6 for other apk /data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/lib/x86_64:/data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 18:10:24.584  2962  2962 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 18:10:24.584  2962  2962 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:10:25.565  2962  2962 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 18:10:25.925  1049  1049 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-25 18:10:25.979  1049  1367 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 18:10:26.109   519   935 D CoreBackPreview: Window{725bf60 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@46fdadd, mPriority=0, mIsAnimationCallback=false}
10-25 18:10:27.045   519   801 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10192, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-25 18:10:27.788   519  2337 I WindowManager: finishDrawing of relaunch: Window{725bf60 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 803ms
10-25 18:10:28.239   519   537 W ziparchive: Unable to open '/data/app/~~4-MzTGYAVYEfCI4qvBGUhg==/com.ghprotocol.app-NmtOETgFOE1YS8e9OdeIAg==/base.dm': No such file or directory
10-25 18:10:28.267   519   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +5s297ms
10-25 18:10:28.335   519  2336 W InputManager-JNI: Input channel object '427f7d0 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 18:10:28.549  1049  1049 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-25 18:10:28.646  1049  1367 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 18:10:29.707   519  1765 D CoreBackPreview: Window{725bf60 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-25 18:10:29.810   519  1094 W InputManager-JNI: Input channel object '725bf60 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-25 18:10:30.558   519  1673 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{175116e com.google.android.gm/10142} BLOCKED
10-25 18:10:30.655   519  2332 D CoreBackPreview: Window{704cae0 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@b857af7, mPriority=0, mIsAnimationCallback=false}
10-25 18:10:31.054  2962  3592 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 18:10:31.055   519  2083 I ImeTracker: com.ghprotocol.app:8935dc8d: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 18:10:31.055   519  2083 I ImeTracker: com.ghprotocol.app:8935dc8d: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 18:10:31.184   519   914 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 18:10:31.184   829   862 V WindowManagerShell: Transition requested: android.os.BinderProxy@5710ebb TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=52421 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@3426fd8} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{a6d9f31 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:31.219  1563  1563 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 18:10:31.466  3626  3626 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 18:10:31.481  3626  3626 I AndroidRuntime: Using default boot image
10-25 18:10:31.481  3626  3626 I AndroidRuntime: Leaving lock profiling enabled
10-25 18:10:31.502  2962  2962 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:10:31.517  2962  2962 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:10:31.727  3676  3676 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:10:31.727  3676  3676 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:10:31.813  3626  3626 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 18:10:31.727  3676  3676 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:10:31.727  3676  3676 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:10:31.838  2962  2962 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:10:31.931  2962  2962 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:10:32.240  2962  2962 D GhDiag  : connect: core.start=true 
10-25 18:10:32.394   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{1978c7a com.android.camera2/10144} BLOCKED
10-25 18:10:32.400   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{ab02c2b com.google.android.devicelockcontroller/10188} BLOCKED
10-25 18:10:32.400   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{eba1888 com.google.android.dialer/10128} BLOCKED
10-25 18:10:32.400   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{9e61221 com.google.android.contacts/10153} BLOCKED
10-25 18:10:32.400   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{701f646 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 18:10:32.709   519  1975 D CoreBackPreview: Window{36810c8 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@1b12083, mPriority=0, mIsAnimationCallback=false}
10-25 18:10:33.105  3626  3626 D AndroidRuntime: Shutting down VM
10-25 18:10:34.201   834   834 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-25 18:10:34.495  3745  3745 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=52777 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 18:10:34.517  2962  2978 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-25 18:10:34.721  2962  2978 I .ghprotocol.app: Background concurrent copying GC freed 102505(5337KB) AllocSpace objects, 27(764KB) LOS objects, 49% free, 6666KB/13MB, paused 75us,7us total 1.377s
10-25 18:10:34.811   829   862 V WindowManagerShell: onTransitionReady android.os.BinderProxy@5710ebb: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f65367c u0 com.ghprotocol.app/.MainActivity)/@0xe54a68f sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2844eed u0 com.ghprotocol.app/.MainActivity)/@0x664ad1c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:10:34.812   829   862 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f65367c u0 com.ghprotocol.app/.MainActivity)/@0xe54a68f sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2844eed u0 com.ghprotocol.app/.MainActivity)/@0x664ad1c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:10:34.812   829   862 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f65367c u0 com.ghprotocol.app/.MainActivity)/@0xe54a68f sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2844eed u0 com.ghprotocol.app/.MainActivity)/@0x664ad1c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:10:34.816   519   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s615ms
10-25 18:10:34.817   519   537 V WindowManager: Sent Transition #7 createdAt=10-25 18:10:31.156 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=52421 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{dc6c486 Task{f9507b3 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7d23f9 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:34.817   519   537 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f65367c u0 com.ghprotocol.app/.MainActivity)/@0x5410443 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{2844eed u0 com.ghprotocol.app/.MainActivity)/@0xc72d5f2 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:10:36.225   829   862 V WindowManagerShell: Transition requested: android.os.BinderProxy@93b954c TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=56374 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@aa3e995} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7340aaa com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:36.243   519   591 I ImeTracker: com.ghprotocol.app:e76ac105: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 18:10:36.249   519   591 I ImeTracker: com.ghprotocol.app:e76ac105: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 18:10:36.253  1563  1563 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 18:10:36.396   519  2330 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 18:10:36.400   519  2330 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 18:10:36.400   519  2330 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 18:10:37.400   519   537 V WindowManager: Sent Transition #8 createdAt=10-25 18:10:35.125 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=56374 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{dc6c486 Task{f9507b3 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2ec0119 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:10:38.319  4136  4136 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 18:10:38.332  4136  4136 I AndroidRuntime: Using default boot image
10-25 18:10:38.332  4136  4136 I AndroidRuntime: Leaving lock profiling enabled
10-25 18:10:39.309  4136  4136 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 18:10:40.428   519  2330 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{8ed7c4a com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:10:40.435   519  1970 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{e556031 com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:10:40.471  4136  4136 D AndroidRuntime: Shutting down VM
10-25 18:10:40.874  1672  1672 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 18:10:41.254  1672  1672 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 18:10:41.255  1672  2999 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 18:10:41.255  1672  2999 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 18:10:41.717   519   995 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 18:10:42.109   519  1093 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 18:10:42.172  2962  2962 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:10:42.247   519  1094 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 18:10:42.248  2962  2962 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@db09da2} — relay loop started
10-25 18:10:42.415  2962  4362 W .ghprotocol.app: Verification of int com.ghprotocol.app.core.Socks5.ipv4Checksum(byte[], int, int) took 164.194ms (377.60 bytecodes/s) (2608B approximate peak alloc)
10-25 18:10:42.469   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{94094f9 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 18:10:42.469   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{f797c3e com.google.android.gm/10142} BLOCKED
10-25 18:10:42.469   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{88fa9f com.google.android.rkpdapp/10173} BLOCKED
10-25 18:10:42.469   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{ca957ec com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:10:42.469   519   573 I AppsFilter: interaction: PackageSetting{32580e9 com.ghprotocol.app/10192} -> PackageSetting{2ddb0db com.google.android.projection.gearhead/10123} BLOCKED
10-25 18:10:42.524  2962  3265 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (56ms)
10-25 18:10:42.609   519   591 I ImeTracker: com.ghprotocol.app:59002030: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 18:10:42.610   519   591 I ImeTracker: com.ghprotocol.app:59002030: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 18:10:42.621  1563  1563 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 18:10:43.494  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.532  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:43.547  1518  4347 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 18:10:43.628  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.652  2962  4362 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:10:43.666  1441  3946 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 18:10:43.705  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:43.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:10:44.051  2962  4412 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:10:44.052  2962  4362 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:10:44.135  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:44.554  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:44.999  2962  4362 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 18:10:45.262  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.266  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 18:10:45.352  2962  4445 D GhDiag  : relay dns -> 168B ok
10-25 18:10:45.361  2962  4444 D GhDiag  : relay dns -> 264B ok
10-25 18:10:45.518  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 18:10:45.523  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 18:10:45.525  2962  4362 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 18:10:45.656  2962  4479 D GhDiag  : relay dns -> 177B ok
10-25 18:10:45.673  2962  4362 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 18:10:45.785  2962  4477 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:10:45.786  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.810  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 18:10:45.841  2962  4488 D GhDiag  : relay dns -> 273B ok
10-25 18:10:45.878  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.879  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.949  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 18:10:45.981  2962  4512 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:10:45.982  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 18:10:45.992  2962  4362 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 18:10:46.544  2962  2978 I .ghprotocol.app: Background young concurrent copying GC freed 63238(5456KB) AllocSpace objects, 0(0B) LOS objects, 18% free, 10MB/13MB, paused 33us,20us total 795.348ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
