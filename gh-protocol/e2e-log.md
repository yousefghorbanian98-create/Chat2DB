## gh-protocol E2E log — 2026-10-25T05:38:34Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T05:28:46Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 05:24 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 05:29 .
drwxr-xr-x 3 runner runner 4096 Oct 25 05:29 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 05:29 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 05:29 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3047
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
WARNING: cannnot unmap ptr 0x7f53a4a01000 as it is in the protected range from 0x7f52a4a00000 to 0x7f53a4c00000
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
INFO         | Boot completed in 37395 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 176
ERROR        | Failed to bind to texture: invalid color buffer.

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
> Task :app:generateDebugBuildConfig
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:parseDebugLocalResources
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugManifest
> Task :app:mergeDebugAssets
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs
> Task :app:compressDebugAssets
> Task :app:mergeExtDexDebug
> Task :app:processDebugResources
> Task :app:mergeLibDexDebug
> Task :app:stripDebugDebugSymbols
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792905981199.json

BUILD SUCCESSFUL in 2m 33s
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
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 60s) ==
WARN: emulator CANNOT reach raw.githubusercontent.com (runner NAT) — pre-seeding app cache
seeded cache: 37417 bytes, meta=1792906275578
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 5450)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a192       5450   338   13665392 175748 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:8872          0.0.0.0:*               LISTEN     
tcp        0      0 10.0.2.16:32884         142.251.152.119:443     CLOSE_WAIT 
tcp      130      0 10.0.2.16:43222         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43248         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43226         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43202         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43194         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:58746         142.251.154.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:55016         172.217.112.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43240         172.217.113.4:443       CLOSE_WAIT 
tcp      130      0 10.0.2.16:43206         172.217.113.4:443       CLOSE_WAIT 
tcp6       0      0 ::ffff:127.0.0.1:36769  [::]:*                  LISTEN     
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
tcp6       0      0 ::ffff:127.0.0.1:37857  [::]:*                  LISTEN     
tcp6       1      0 ::ffff:10.0.2.16:40184  ::ffff:142.251.156.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:51360  ::ffff:142.251.155.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:41282  ::ffff:142.251.163.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:53134  ::ffff:172.253.122.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:38688  ::ffff:192.178.155.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:34170  ::ffff:172.217.114.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:49266  ::ffff:172.217.116.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:40340  ::ffff:192.179.18.9:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:41386  ::ffff:172.253.115.:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:51742  ::ffff:142.250.31.9:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:49114  ::ffff:64.233.180.1:443 CLOSE_WAIT 
tcp6       1      0 ::ffff:10.0.2.16:41286  ::ffff:142.251.163.:443 CLOSE_WAIT 
tcp6       0      0 ::ffff:10.0.2.16:45440  ::ffff:172.253.63.:5228 ESTABLISHED
tcp6       1      0 ::ffff:10.0.2.16:34166  ::ffff:172.217.114.:443 CLOSE_WAIT 
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{c485375 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(291, 691 - 790, 1771)
    isSleeping=false
    topResumedActivity=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{3921598 5450:com.ghprotocol.app/u0a192}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.1 fontWeightAdjustment=0}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
        backgroundColor=ff303030 statusBarColor=0 navigationBarColor=0
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2 waitingToShow=true
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-7m7s892ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=true
    * Hist  #0: ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{3921598 5450:com.ghprotocol.app/u0a192}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}
      taskAffinity=10192:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
        mOverrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      ResolvedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} s.2 ?fontWeightAdjustment}
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{e3d63a4 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      nowVisible=false lastVisibleTime=-7m14s606ms
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2400 rng=1080x1017-2400x2337
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@31101906
  deepestLastOrientationSource=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 310mcc260mnc [en_US] ldltr sw411dp w411dp h890dp 420dpi nrml long port finger qwerty/v/v dpad/v winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2400) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.36 fontWeightAdjustment=0}
  mLayoutSeq=89
  mCurrentFocus=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mFocusedApp=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  mSystemGestureExclusion=SkRegion()
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}
      mLastFocusedRootTask=Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{c485375 #8 type=standard A=10192:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity t8}
      * Task{2530ba0 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{9af8fe0 #7 type=home I=com.google.android.apps.nexuslauncher/.NexusLauncherActivity U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{ae09e3 u0 com.google.android.apps.nexuslauncher/.NexusLauncherActivity t7}
      * Task{4594862 #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{409bab0 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    isKeyguardShowing=false
    mTopGestureHost=Window{b2427cd u0 StatusBar}
    mFocusedWindow=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopFullscreenOpaqueWindowState=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mSystemBarColorApps={ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity t8}}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{LIGHT_STATUS_BARS bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_90={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][1080,2400], configFrame=[0,63][1080,2400]}
      ROTATION_270={nonDecorInsets=[0,0][0,0], configInsets=[0,63][0,0], nonDecorFrame=[0,0][2400,1080], configFrame=[0,63][2400,1080]}
--
        InsetsSource id=112b0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
    Control map:
      Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}:
        InsetsSourceControl: {3 mType=ime mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0}}
        InsetsSourceControl: {112b0000 mType=statusBars initiallyVisible mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=63, right=0, bottom=0}}
    InsetsSourceProviders:
      InsetsSourceProvider
        mSource=InsetsSource id=112b0006 type=tappableElement frame=[0,0][1080,63] visible=true flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 0 - 1080, 63)
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{b2427cd u0 StatusBar}
--
        mWindowContainer=Window{b2427cd u0 StatusBar}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=b2427cd StatusBar)/@0x766bace - animation-leash of insets_animation)/@0x862ad1c
        mControlTarget=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
      ImeInsetsSourceProvider
        mSource=InsetsSource id=3 type=ime frame=[0,0][0,0] visible=false flags= insetsRoundedCornerFrame=false
        mSourceFrame=Rect(0, 2400 - 1080, 2400)
        mControl=InsetsSourceControl mId=3 mType=ime mLeash=Surface(name=Surface(name=ede571b InputMethod)/@0x28a0e91 - animation-leash of insets_animation)/@0x26a6d25 mInitiallyVisible=false mSurfacePosition=Point(0, 0) mInsetsHint=Insets{left=0, top=0, right=0, bottom=0} mSkipAnimationOnce=false
        mIsLeashReadyForDispatching=true
        mWindowContainer=Window{ede571b u0 InputMethod}
        mAdapter=ControlAdapter mCapturedLeash=Surface(name=Surface(name=ede571b InputMethod)/@0x28a0e91 - animation-leash of insets_animation)/@0x26a6d25
        mControlTarget=Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
        mImeShowing=false

  KeyguardController:
    mKeyguardShowing=false
    mAodShowing=false
    mKeyguardGoingAway=false
   KeyguardShowing=false AodShowing=false KeyguardGoingAway=false DismissalRequested=false  Occluded=false DismissingKeyguardActivity=null TurnScreenOnActivity=null at display=0
    mDismissalRequested=false
--
        (multi-window) Task{bddddf3 #3 type=undefined}
        (multi-window) Task{409bab0 #4 type=undefined}
        (fullscreen) Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{3921598 5450:com.ghprotocol.app/u0a192}]
  NumNonAppVisibleWindowUidMap:[ 10168:1]
app filesDir/xray:
total 79624
drwx------ 2 u0_a192 u0_a192     4096 2026-10-25 05:31 .
drwxrwxrwx 3 u0_a192 u0_a192     4096 2026-10-25 05:31 ..
-rwx--x--x 1 u0_a192 u0_a192 38872056 2026-10-25 05:31 Xray
-rw------- 1 u0_a192 u0_a192 36282168 2026-10-25 05:31 Xray-arm64-v8a
-rw------- 1 u0_a192 u0_a192  3977011 2026-10-25 05:31 geoip.dat
-rw------- 1 u0_a192 u0_a192  2358471 2026-10-25 05:31 geosite.dat
xray-err.log:
GhDiag (connect-flow trace):
--------- beginning of main
10-25 05:31:23.817  5450  5450 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 05:31:23.817  5450  5450 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 05:31:24.285  5450  5450 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-25 05:31:24.286  5450  5450 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
 resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@b4de6e0} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{dc3bd99 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:31:15.530   522   550 I ActivityManager: Start proc 5450:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 05:31:15.537   522  2228 D CoreBackPreview: Window{e0016f3 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@37b2f4f, mPriority=0, mIsAnimationCallback=false}
10-25 05:31:15.561  5450  5450 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 05:31:15.635  5450  5450 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 05:31:15.639  5450  5450 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 05:31:15.639  5450  5450 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 05:31:15.844   522   539 V WindowManager: Sent Transition #6 createdAt=10-25 05:31:15.492 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=100406 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6e7f961 Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{c6ec86 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:31:15.846   522   539 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{6e7f961 Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x9d603e5 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{667b947 Task{2530ba0 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xab7b967 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:31:16.145  5450  5450 W ziparchive: Unable to open '/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.dm': No such file or directory
10-25 05:31:16.145  5450  5450 W ziparchive: Unable to open '/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.dm': No such file or directory
10-25 05:31:16.360  5450  5450 D nativeloader: Configuring clns-6 for other apk /data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/lib/x86_64:/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 05:31:16.368  5450  5450 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 05:31:16.368  5450  5450 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 05:31:16.759  5450  5450 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:31:16.759  5450  5450 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 05:31:16.759  5450  5450 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 05:31:16.759  5450  5450 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 05:31:16.760  5450  5450 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:31:16.760  5450  5450 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 05:31:16.760  5450  5450 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 05:31:16.810   522   822 D CoreBackPreview: Window{e3d63a4 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@192fdd4, mPriority=0, mIsAnimationCallback=false}
10-25 05:31:17.751   522   539 W ziparchive: Unable to open '/data/app/~~qWdq8PL3JbKosp0K7JAddg==/com.ghprotocol.app-eH6VgHKPoE3Th57Ezf5O4g==/base.dm': No such file or directory
10-25 05:31:17.752   522   539 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +2s261ms
10-25 05:31:17.773   522  2206 D CoreBackPreview: Window{e0016f3 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 05:31:17.774   522  2009 W InputManager-JNI: Input channel object 'e0016f3 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 05:31:17.871   522   822 I ImeTracker: com.ghprotocol.app:2ab1b500: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 05:31:17.871   522   822 I ImeTracker: com.ghprotocol.app:2ab1b500: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 05:31:17.876  1528  1528 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 05:31:19.974   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{fceb4fc com.google.android.contacts/10154} BLOCKED
10-25 05:31:22.424  5450  5655 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 05:31:23.559   833   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@ad867ff TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=108462 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@c0e29cc} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{28c2415 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:31:23.559   522  2231 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 05:31:23.817  5450  5450 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 05:31:23.817  5450  5450 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 05:31:24.285  5450  5450 D GhDiag  : connect: ensureInstalled=false version=null err=Xray version unreadable
10-25 05:31:24.286  5450  5450 D GhDiag  : connect: FAILED — core unavailable/old (min=26.6.27)
10-25 05:31:24.284  5675  5675 W .ghprotocol.app: type=1400 audit(0.0:45): avc:  granted  { execute } for  name="Xray" dev="dm-40" ino=147517 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c192,c256,c512,c768 tclass=file app=com.ghprotocol.app
10-25 05:31:24.284  5675  5675 W .ghprotocol.app: type=1400 audit(0.0:46): avc:  denied  { execute_no_trans } for  path="/data/data/com.ghprotocol.app/files/xray/Xray" dev="dm-40" ino=147517 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:app_data_file:s0:c192,c256,c512,c768 tclass=file permissive=0 app=com.ghprotocol.app
10-25 05:31:24.317   522  2230 D CoreBackPreview: Window{3676010 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@ab07d1b, mPriority=0, mIsAnimationCallback=false}
10-25 05:31:24.492   522   539 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +934ms
10-25 05:31:24.492   522   539 V WindowManager: Sent Transition #7 createdAt=10-25 05:31:23.555 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=108462 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6e7f961 Task{c485375 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{14db5fc com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 05:31:24.492   522   539 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity)/@0x84c87ce sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity)/@0xb3154c9 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:31:24.493   833   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@ad867ff: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity)/@0x5e7f32a sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity)/@0xc55851b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:31:24.494   833   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity)/@0x5e7f32a sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity)/@0xc55851b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:31:24.499   833   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{3f6f70d u0 com.ghprotocol.app/.MainActivity)/@0x5e7f32a sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{f29faac u0 com.ghprotocol.app/.MainActivity)/@0xc55851b sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 05:31:24.755   522  2230 I ImeTracker: com.ghprotocol.app:884a321d: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 05:31:24.755   522  2230 I ImeTracker: com.ghprotocol.app:884a321d: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 05:31:24.756  1528  1528 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 05:31:29.135   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{75b6dad com.google.android.contacts/10154} BLOCKED
10-25 05:31:32.193  5790  5790 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:31:32.197  5790  5790 I AndroidRuntime: Using default boot image
10-25 05:31:32.197  5790  5790 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:31:32.383  5790  5790 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:31:33.533  5790  5790 D AndroidRuntime: Shutting down VM
10-25 05:31:41.740   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{b47f209 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 05:31:43.508   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{899de5b com.google.android.contacts/10154} BLOCKED
10-25 05:31:47.149  5864  5864 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:31:47.153  5864  5864 I AndroidRuntime: Using default boot image
10-25 05:31:47.153  5864  5864 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:31:47.239  5864  5864 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:31:48.293  5864  5864 D AndroidRuntime: Shutting down VM
10-25 05:32:01.395  5894  5894 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:32:01.398  5894  5894 I AndroidRuntime: Using default boot image
10-25 05:32:01.398  5894  5894 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:32:01.479  5894  5894 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:32:02.548  5894  5894 D AndroidRuntime: Shutting down VM
10-25 05:32:14.934   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{878f888 com.google.android.contacts/10154} BLOCKED
10-25 05:32:15.693  5988  5988 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:32:15.696  5988  5988 I AndroidRuntime: Using default boot image
10-25 05:32:15.696  5988  5988 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:32:15.773  5988  5988 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:32:16.845  5988  5988 D AndroidRuntime: Shutting down VM
10-25 05:32:24.938   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{8b3a9c7 com.google.android.contacts/10154} BLOCKED
10-25 05:32:29.996  6046  6046 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:32:30.000  6046  6046 I AndroidRuntime: Using default boot image
10-25 05:32:30.000  6046  6046 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:32:30.080  6046  6046 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:32:31.144  6046  6046 D AndroidRuntime: Shutting down VM
10-25 05:32:44.236  6086  6086 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:32:44.239  6086  6086 I AndroidRuntime: Using default boot image
10-25 05:32:44.239  6086  6086 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:32:44.319  6086  6086 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:32:45.378  6086  6086 D AndroidRuntime: Shutting down VM
10-25 05:32:58.517  6119  6119 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:32:58.521  6119  6119 I AndroidRuntime: Using default boot image
10-25 05:32:58.521  6119  6119 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:32:58.601  6119  6119 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:32:59.671  6119  6119 D AndroidRuntime: Shutting down VM
10-25 05:33:12.885  6157  6157 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:33:12.889  6157  6157 I AndroidRuntime: Using default boot image
10-25 05:33:12.889  6157  6157 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:33:12.969  6157  6157 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:33:14.024  6157  6157 D AndroidRuntime: Shutting down VM
10-25 05:33:27.142  6182  6182 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:33:27.145  6182  6182 I AndroidRuntime: Using default boot image
10-25 05:33:27.145  6182  6182 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:33:27.225  6182  6182 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:33:28.283  6182  6182 D AndroidRuntime: Shutting down VM
10-25 05:33:41.416  6217  6217 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:33:41.420  6217  6217 I AndroidRuntime: Using default boot image
10-25 05:33:41.420  6217  6217 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:33:41.499  6217  6217 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:33:42.543  6217  6217 D AndroidRuntime: Shutting down VM
10-25 05:33:55.658  6243  6243 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:33:55.662  6243  6243 I AndroidRuntime: Using default boot image
10-25 05:33:55.662  6243  6243 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:33:55.742  6243  6243 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:33:56.805  6243  6243 D AndroidRuntime: Shutting down VM
10-25 05:34:09.979  6275  6275 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:34:09.982  6275  6275 I AndroidRuntime: Using default boot image
10-25 05:34:09.982  6275  6275 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:34:10.059  6275  6275 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:34:11.125  6275  6275 D AndroidRuntime: Shutting down VM
10-25 05:34:24.233  6299  6299 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:34:24.237  6299  6299 I AndroidRuntime: Using default boot image
10-25 05:34:24.237  6299  6299 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:34:24.314  6299  6299 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:34:25.358  6299  6299 D AndroidRuntime: Shutting down VM
10-25 05:34:38.473  6326  6326 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:34:38.477  6326  6326 I AndroidRuntime: Using default boot image
10-25 05:34:38.477  6326  6326 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:34:38.557  6326  6326 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:34:39.629  6326  6326 D AndroidRuntime: Shutting down VM
10-25 05:34:52.738  6384  6384 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:34:52.742  6384  6384 I AndroidRuntime: Using default boot image
10-25 05:34:52.742  6384  6384 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:34:52.821  6384  6384 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:34:53.874  6384  6384 D AndroidRuntime: Shutting down VM
10-25 05:35:06.920  6408  6408 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:35:06.924  6408  6408 I AndroidRuntime: Using default boot image
10-25 05:35:06.924  6408  6408 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:35:07.003  6408  6408 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:35:08.047  6408  6408 D AndroidRuntime: Shutting down VM
10-25 05:35:21.176  6446  6446 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:35:21.179  6446  6446 I AndroidRuntime: Using default boot image
10-25 05:35:21.179  6446  6446 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:35:21.266  6446  6446 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:35:22.315  6446  6446 D AndroidRuntime: Shutting down VM
10-25 05:35:35.446  6484  6484 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:35:35.450  6484  6484 I AndroidRuntime: Using default boot image
10-25 05:35:35.450  6484  6484 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:35:35.533  6484  6484 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:35:36.580  6484  6484 D AndroidRuntime: Shutting down VM
10-25 05:35:49.737  6509  6509 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:35:49.740  6509  6509 I AndroidRuntime: Using default boot image
10-25 05:35:49.740  6509  6509 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:35:49.823  6509  6509 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:35:50.892  6509  6509 D AndroidRuntime: Shutting down VM
10-25 05:36:03.973  6536  6536 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:36:03.977  6536  6536 I AndroidRuntime: Using default boot image
10-25 05:36:03.977  6536  6536 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:36:04.058  6536  6536 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:36:05.118  6536  6536 D AndroidRuntime: Shutting down VM
10-25 05:36:18.326  6613  6613 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:36:18.334  6613  6613 I AndroidRuntime: Using default boot image
10-25 05:36:18.334  6613  6613 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:36:18.441  6613  6613 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:36:19.510  6613  6613 D AndroidRuntime: Shutting down VM
10-25 05:36:21.366   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{559134d com.google.android.contacts/10154} BLOCKED
10-25 05:36:31.381   522   573 I AppsFilter: interaction: PackageSetting{b4461ef com.ghprotocol.app/10192} -> PackageSetting{1493d43 com.google.android.contacts/10154} BLOCKED
10-25 05:36:32.597  6709  6709 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:36:32.600  6709  6709 I AndroidRuntime: Using default boot image
10-25 05:36:32.600  6709  6709 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:36:32.681  6709  6709 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:36:33.735  6709  6709 D AndroidRuntime: Shutting down VM
10-25 05:36:46.781  6735  6735 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:36:46.785  6735  6735 I AndroidRuntime: Using default boot image
10-25 05:36:46.785  6735  6735 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:36:46.863  6735  6735 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:36:47.913  6735  6735 D AndroidRuntime: Shutting down VM
10-25 05:37:00.982  6760  6760 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:37:00.986  6760  6760 I AndroidRuntime: Using default boot image
10-25 05:37:00.986  6760  6760 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:37:01.067  6760  6760 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:37:02.119  6760  6760 D AndroidRuntime: Shutting down VM
10-25 05:37:15.224  6786  6786 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:37:15.227  6786  6786 I AndroidRuntime: Using default boot image
10-25 05:37:15.227  6786  6786 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:37:15.311  6786  6786 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:37:16.359  6786  6786 D AndroidRuntime: Shutting down VM
10-25 05:37:29.441  6810  6810 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:37:29.445  6810  6810 I AndroidRuntime: Using default boot image
10-25 05:37:29.445  6810  6810 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:37:29.526  6810  6810 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:37:30.568  6810  6810 D AndroidRuntime: Shutting down VM
10-25 05:37:43.653  6837  6837 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:37:43.656  6837  6837 I AndroidRuntime: Using default boot image
10-25 05:37:43.656  6837  6837 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:37:43.735  6837  6837 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:37:44.785  6837  6837 D AndroidRuntime: Shutting down VM
10-25 05:37:57.846  6860  6860 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:37:57.849  6860  6860 I AndroidRuntime: Using default boot image
10-25 05:37:57.849  6860  6860 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:37:57.928  6860  6860 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:37:58.981  6860  6860 D AndroidRuntime: Shutting down VM
10-25 05:38:12.051  6885  6885 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:38:12.055  6885  6885 I AndroidRuntime: Using default boot image
10-25 05:38:12.055  6885  6885 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:38:12.136  6885  6885 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:38:13.196  6885  6885 D AndroidRuntime: Shutting down VM
10-25 05:38:26.307  6916  6916 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 05:38:26.311  6916  6916 I AndroidRuntime: Using default boot image
10-25 05:38:26.311  6916  6916 I AndroidRuntime: Leaving lock profiling enabled
10-25 05:38:26.391  6916  6916 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 05:38:27.439  6916  6916 D AndroidRuntime: Shutting down VM


