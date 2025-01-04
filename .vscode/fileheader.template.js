/**
 * @author        Haiyang_Liao
 * @affiliation   Nanjing_University
 * @email         haiyangliao@nju.edu.cn
 * @date          ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
 */
class CustomLanguageProvider extends globalThis.FileheaderLanguageProvider {
  /**
   * @type {string[]}
   */
  languages = [
    "javascript",
    "typescript",
    "javascriptreact",
    "typescriptreact",
  ];

  /**
   * @type {string=}
   */
  blockCommentStart = "/*";

  /**
   * @type {string=}
   */
  blockCommentEnd = "*/";

  /**
   * get your template when document language matched
   * @param {ITemplateFunction} tpl template function, it is a tagged function, support nested interpolation
   * @param {FileheaderVariable} variables template variables
   * @returns {Template}
   */
  getTemplate(tpl, variables) {
    // prettier-ignore
    return tpl
`/*
 * @author        Haiyang Liao
 * @affiliation   Nanjing University
 * @email         haiyangliao@nju.edu.cn
 * @date          ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}
 */`;
  }
}

// export your provider classes
module.exports = [CustomLanguageProvider];
